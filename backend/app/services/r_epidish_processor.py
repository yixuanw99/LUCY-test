# app/services/r_epidish_cell_proportion.py
import pandas as pd
import logging
import os
import subprocess
import json
import io
import tempfile
from app.services.gcs_storage import GCSStorage
from app.core.config import settings
from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

# print(f"Project root: {project_root}")
# print(f"Python path: {sys.path}")
# print(f"Current working directory: {os.getcwd()}")

from app.db import models
from app.db.session import SessionLocal

class EpiDISHProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.backend_root = Path(__file__).resolve().parents[2]
        self.r_script_path = settings.EPIDISH_R_SCRIPT_PATH
        self.r_executable = settings.R_EXECUTABLE
        self.gcs_storage = GCSStorage()

    def run_epidish_with_csv(self, gcs_file_path: str) -> pd.DataFrame:
        '''
        使用 R 的 EpiDISH 包處理 CSV 文件，並返回細胞比例的 DataFrame
        
        :param gcs_file_path: 包含甲基化數據的 CSV 文件的路徑
        :return: EpiDISH 處理後的細胞比例 DataFrame
        '''
        self.logger.info(f"Processing CSV file with EpiDISH: {gcs_file_path}")

        if not self.r_script_path:
            raise ValueError("EPIDISH_R_SCRIPT_PATH environment variable is not set")
        
        if not os.path.exists(self.r_script_path):
            raise FileNotFoundError(f"R script not found at {self.r_script_path}")
        
        # Download the file content from GCS as string
        csv_content = self.gcs_storage.download_as_text_utf8(gcs_file_path)

        # Create a temporary file in memory
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as temp_file:
            temp_file.write(csv_content)
            temp_file_path = temp_file.name

        try:
            result = subprocess.run(
                [self.r_executable, self.r_script_path, temp_file_path],
                capture_output=True,
                text=True,
                check=True
            )

            output_lines = result.stdout.strip().split('\n')
            json_output = output_lines[-1]

            try:
                output = json.loads(json_output)
            except json.JSONDecodeError as json_error:
                self.logger.error(f"Failed to parse R script output as JSON: {json_error}")
                self.logger.error(f"R script output: {json_output}")
                raise
            
            if output['status'] == 'success':
                self.logger.info("EpiDISH processing completed successfully")
                self.logger.info(f"Output: {output}")
                
                cell_proportion_data = output['data']['cell_proportion']
                
                df = pd.DataFrame(cell_proportion_data)
                df.set_index('SampleID', inplace=True)
                
                return df
            
            else:
                self.logger.error(f"R script execution failed: {output.get('message', 'Unknown error')}")
                raise RuntimeError(output.get('message', 'Unknown error'))
        except subprocess.CalledProcessError as e:
            self.logger.error(f"R script execution failed: {e.stderr}")
            raise
        except Exception as e:
            self.logger.error(f"Other error in processing CSV file with EpiDISH: {str(e)}")
            raise
        finally:
            # Remove the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def save_cell_proportions(self, cell_proportions: pd.DataFrame, batch_name: str) -> str:
        '''
        保存細胞比例數據到 CSV 文件並更新數據庫
        
        :param cell_proportions: 細胞比例的 DataFrame
        :param batch_name: 樣本名稱，用於生成文件名
        :return: 保存的文件的相對路徑
        '''
        gcs_path = f"data/cell_proportions/{batch_name}_cell_proportions.csv"

        # 將 DataFrame 轉換為 CSV 格式的字符串
        csv_buffer = io.StringIO()
        cell_proportions.to_csv(csv_buffer, index=True)
        csv_string = csv_buffer.getvalue()

        # 直接上傳字符串內容到 GCS
        gcs_url = self.gcs_storage.upload_string(csv_string, gcs_path)
        self.logger.info(f"Cell proportions saved to GCS: {gcs_url}")
        
        # Update database
        db = SessionLocal()
        try:
            # 獲取所有 sample_name
            sample_names = cell_proportions.index.tolist()
            
            # 批量查詢 sample_id
            samples = db.query(models.SampleData).filter(models.SampleData.sample_name.in_(sample_names)).all()
            
            # 創建 sample_name 到 sample 對象的映射
            sample_map = {sample.sample_name: sample for sample in samples}
            
            # 更新每個樣本的 cell_proportion_path
            for sample_name in sample_names:
                sample = sample_map.get(sample_name)
                if sample:
                    sample.cell_proportion_path = gcs_url
                else:
                    self.logger.warning(f"Sample with name {sample_name} not found in database")
            
            db.commit()
            self.logger.info(f"Updated cell_proportion_path for {len(samples)} samples")
        except Exception as e:
            db.rollback()
            self.logger.error(f"Error updating database: {str(e)}")
        finally:
            db.close()
        
        return gcs_url


if __name__ == "__main__":
    # import argparse

    # parser = argparse.ArgumentParser(description="Process CSV file with EpiDISH")
    # parser.add_argument("gcs_file_path", help="Path to the CSV file containing methylation data")
    # parser.add_argument("--batch_name", help="Name of the batch for output file", required=True)
    # args = parser.parse_args()

    processor = EpiDISHProcessor()

    try:
        # 示例用法
        # python app/services/r_epidish_processor.py "data/processed_beta_table/our_all_samples_processed.csv" --batch_name our_all_samples
        result = processor.run_epidish_with_csv("data/processed_beta_table/our_all_samples_processed.csv")
        if isinstance(result, pd.DataFrame):
            print("Processing completed. Sample of cell proportions:")
            print(result.head())
            print(f"\nTotal number of samples: {len(result)}")
            
            relative_path = processor.save_cell_proportions(result, "our_all_samples")
            print(f"Cell proportions saved. Relative path: {relative_path}")
        else:
            print("Processing did not return a DataFrame.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
