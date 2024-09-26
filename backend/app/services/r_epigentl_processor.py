# app/services/r_epigentl_processor.py
import pandas as pd
import logging
import os
import subprocess
import json
import io
from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from app.db import models
from app.db.session import SessionLocal
from app.services.gcs_storage import GCSStorage
from app.core.config import settings

class EpigenTLProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.backend_root = Path(__file__).resolve().parents[2]
        self.r_script_path = settings.EPIGENTL_R_SCRIPT_PATH
        self.r_executable = settings.R_EXECUTABLE
        self.resource_dir = self.backend_root / 'app' / 'resources'
        self.probes_file = self.resource_dir / 'model_probes' / 'EpigenTL_probes.csv'
        self.ex_sample_file = self.resource_dir / 'model_probes' / 'ExSample_SalivaCpGs.csv'
        self.gcs_storage = GCSStorage()

    def read_model_probes(self) -> pd.Series:
        """
        Read the model probes from a CSV file.
        
        :return: Series of model probes
        """
        model_probes = pd.read_csv(self.probes_file, header=None, names=['probeID'])
        return model_probes['probeID']

    def preprocess_beta_table(self, beta_table: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess beta table by filtering and imputing missing values.
        
        :param beta_table: Original beta table
        :return: Preprocessed beta table
        """
        self.logger.info("Preprocessing beta table")
        
        EpigenTL_Cpgs = self.read_model_probes()
        
        # Read ExSample_SalivaCpGs
        ExSample_Saliva_beta_table = pd.read_csv(self.ex_sample_file)
        # 第一列是索引，但没有列名，我们给它一个名字
        ExSample_Saliva_beta_table.index.name = 'sample_id'
        # 重置索引，使第一列成为一个普通列
        ExSample_Saliva_beta_table = ExSample_Saliva_beta_table.reset_index()
        # 现在列名就是CpG探针ID
        
        # Filter beta_table
        beta_table_filtered = beta_table[beta_table.index.isin(EpigenTL_Cpgs)].copy()
        
        # Find missing CpGs
        missing_cpgs = EpigenTL_Cpgs[~EpigenTL_Cpgs.isin(beta_table.index)]
        
        # Impute missing CpGs
        for cpg in missing_cpgs:
            if cpg in ExSample_Saliva_beta_table.columns:
                mean_value = ExSample_Saliva_beta_table[cpg].mean()
                beta_table_filtered.loc[cpg] = mean_value
        
        return beta_table_filtered
    
    def run_epigentl_with_csv(self, csv_file_path: str) -> pd.DataFrame:
        '''
        使用 R 的 EpigenTL 包處理 CSV 文件，並返回 EpigenTL 結果的 DataFrame
        
        :param csv_file_path: 包含甲基化數據的 CSV 文件的路徑
        :return: EpigenTL 處理後的結果 DataFrame
        '''
        self.logger.info(f"Processing CSV file with EpigenTL: {csv_file_path}")

        if not self.r_script_path:
            raise ValueError("EPIGENTL_R_SCRIPT_PATH environment variable is not set")
        
        if not os.path.exists(self.r_script_path):
            raise FileNotFoundError(f"R script not found at {self.r_script_path}")
        
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"CSV file not found at {csv_file_path}")
        
        # Read and preprocess the beta table
        beta_table = pd.read_csv(csv_file_path, index_col='probeID')
        preprocessed_beta_table = self.preprocess_beta_table(beta_table)
        
        # Save preprocessed beta table to a temporary file
        temp_csv_path = csv_file_path.replace('.csv', '_preprocessed.csv')
        preprocessed_beta_table.to_csv(temp_csv_path)

        r_script_dir = os.path.dirname(self.r_script_path)
        epigentl_source_functions_path = os.path.join(r_script_dir, 'EpigenTL_SourceFunctions.R')


        try:
            result = subprocess.run(
                [self.r_executable, self.r_script_path, temp_csv_path, epigentl_source_functions_path],
                capture_output=True,
                text=True,
                check=True
            )

            self.logger.info("R script output:")
            self.logger.info(result.stdout)

            output_lines = result.stdout.strip().split('\n')
            json_output = output_lines[-1]

            try:
                output = json.loads(json_output)
            except json.JSONDecodeError as json_error:
                self.logger.error(f"Failed to parse R script output as JSON: {json_error}")
                self.logger.error(f"R script output: {json_output}")
                raise
            
            if output['status'] == 'success':
                self.logger.info("EpigenTL processing completed successfully")
                
                epigentl_data = output['data']['epigentl_results']
                
                df = pd.DataFrame(epigentl_data)
                df.set_index('SampleID', inplace=True)
                
                return df
            
            else:
                self.logger.error(f"R script execution failed: {output.get('message', 'Unknown error')}")
                raise RuntimeError(output.get('message', 'Unknown error'))
        except subprocess.CalledProcessError as e:
            self.logger.error(f"R script execution failed: {e.stderr}")
            raise
        except Exception as e:
            self.logger.error(f"Other error in processing CSV file with EpigenTL: {str(e)}")
            raise
        finally:
            # Remove the temporary preprocessed CSV file
            if os.path.exists(temp_csv_path):
                os.remove(temp_csv_path)

    def run_epigentl_with_csv_fromGCS(self, gcs_file_path: str) -> pd.DataFrame:
        '''
        使用 R 的 EpigenTL 包處理 CSV 文件，並返回 EpigenTL 結果的 DataFrame
        
        :param gcs_file_path: 包含甲基化數據的 CSV 文件的路徑
        :return: EpigenTL 處理後的結果 DataFrame
        '''
        self.logger.info(f"Processing CSV file with EpigenTL: {gcs_file_path}")

        if not self.r_script_path:
            raise ValueError("EPIGENTL_R_SCRIPT_PATH environment variable is not set")
        
        if not os.path.exists(self.r_script_path):
            raise FileNotFoundError(f"R script not found at {self.r_script_path}")
        
        # Download the file content from GCS as string
        csv_content = self.gcs_storage.download_as_text_utf8(gcs_file_path)
        
        # Read and preprocess the beta table
        beta_table = pd.read_csv(io.StringIO(csv_content), index_col='probeID')
        preprocessed_beta_table = self.preprocess_beta_table(beta_table)
        
        # Save preprocessed beta table to a temporary file in memory
        temp_preprocessed_file = '/tmp/temp_epigentl_preprocessed.csv'
        preprocessed_beta_table.to_csv(temp_preprocessed_file)

        r_script_dir = os.path.dirname(self.r_script_path)
        epigentl_source_functions_path = os.path.join(r_script_dir, 'EpigenTL_SourceFunctions.R')


        try:
            result = subprocess.run(
                [self.r_executable, self.r_script_path, temp_preprocessed_file, epigentl_source_functions_path],
                capture_output=True,
                text=True,
                check=True
            )

            self.logger.info("R script output:")
            self.logger.info(result.stdout)

            output_lines = result.stdout.strip().split('\n')
            json_output = output_lines[-1]

            try:
                output = json.loads(json_output)
            except json.JSONDecodeError as json_error:
                self.logger.error(f"Failed to parse R script output as JSON: {json_error}")
                self.logger.error(f"R script output: {json_output}")
                raise
            
            if output['status'] == 'success':
                self.logger.info("EpigenTL processing completed successfully")
                
                epigentl_data = output['data']['epigentl_results']
                
                df = pd.DataFrame(epigentl_data)
                df.set_index('SampleID', inplace=True)
                
                return df
            
            else:
                self.logger.error(f"R script execution failed: {output.get('message', 'Unknown error')}")
                raise RuntimeError(output.get('message', 'Unknown error'))
        except subprocess.CalledProcessError as e:
            self.logger.error(f"R script execution failed: {e.stderr}")
            raise
        except Exception as e:
            self.logger.error(f"Other error in processing CSV file with EpigenTL: {str(e)}")
            raise
        finally:
            # Remove the temporary file
            if os.path.exists(temp_preprocessed_file):
                os.remove(temp_preprocessed_file)

    def save_epigentl_results(self, epigentl_results: pd.DataFrame, batch_name: str) -> str:
        '''
        保存 EpigenTL 結果到 CSV 文件並更新數據庫
        
        :param epigentl_results: EpigenTL 結果的 DataFrame
        :param batch_name: 樣本名稱，用於生成文件名
        :return: 保存的文件的相對路徑
        '''
        gcs_path = f"data/epigentl_results/{batch_name}_epigentl_results.csv"
        # 將 DataFrame 轉換為 CSV 格式的字符串
        csv_buffer = io.StringIO()
        epigentl_results.to_csv(csv_buffer, index=True)
        csv_string = csv_buffer.getvalue()

        # 直接上傳字符串內容到 GCS
        gcs_url = self.gcs_storage.upload_string(csv_string, gcs_path)
        self.logger.info(f"EpigenTL results saved to GCS: {gcs_url}")

        
        # TODO: update database with the GCS path
        
        return gcs_url


if __name__ == "__main__":
    processor = EpigenTLProcessor()

    try:
        # 示例用法
        # result = processor.run_epigentl_with_csv_fromGCS("data/processed_beta_table/report_test01_processed.csv")
        result = processor.run_epigentl_with_csv("D:/Github/LUCY-test/backend/data/processed_beta_table/report_test01_processed.csv")
        if isinstance(result, pd.DataFrame):
            print("Processing completed. Sample of EpigenTL results:")
            print(result.head())
            print(f"\nTotal number of samples: {len(result)}")
            
            relative_path = processor.save_epigentl_results(result, "our_all_samples")
            print(f"EpigenTL results saved. Relative path: {relative_path}")
        else:
            print("Processing did not return a DataFrame.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")