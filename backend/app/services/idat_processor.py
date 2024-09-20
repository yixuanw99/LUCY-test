# app/services/idat_processor.py
import pandas as pd
import logging
import os
import subprocess
import json
import tempfile
import time
import io
from pathlib import Path
import sys
from google.cloud import storage
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from app.core.config import settings
from app.services.gcs_storage import GCSStorage
from app.db.session import SessionLocal
from app.db import models


class IDATProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.backend_root = Path(__file__).resolve().parents[2]
        self.r_script_path = settings.CHAMP_R_SCRIPT_PATH
        self.r_executable = settings.R_EXECUTABLE
        self.gcs_storage = GCSStorage()

    def process_idat(self, pd_file_path, idat_file_path) -> pd.DataFrame:
        '''
        使用 R 腳本處理 IDAT 文件，並返回處理後的 DataFrame
        
        :param pd_file_path: Sample Sheet CSV 文件的路徑
        :param idat_file_path: 包含 IDAT 文件的目錄的路徑
        :return: ChAMP處理後的 DataFrame
        '''
        self.logger.info(f"Processing IDAT file: {idat_file_path}")
        self.logger.info(f"Using Sample Sheet: {pd_file_path}")

        if not self.r_script_path:
            raise ValueError("R_SCRIPT_PATH environment variable is not set")
        
        if not os.path.exists(self.r_script_path):
            raise FileNotFoundError(f"R script not found at {self.r_script_path}")
        
        if not os.path.exists(pd_file_path):
            raise FileNotFoundError(f"Sample Sheet not found at {pd_file_path}")
        
        if not os.path.exists(idat_file_path):
            raise FileNotFoundError(f"IDAT directory not found at {idat_file_path}")
        
        try:
            result = subprocess.run(
                [self.r_executable, self.r_script_path, pd_file_path, idat_file_path],
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
                self.logger.error(f"R script output: {output_lines}")
                raise

            if output['status'] == 'success':
                self.logger.info("IDAT processing completed successfully")
                beta_table = output['data']['beta_table']
                rownames = output['data']['rownames']
                colnames = output['data']['colnames']
                return pd.DataFrame(beta_table, index=rownames, columns=colnames)
            else:
                self.logger.error(f"R script execution failed: {output['message']}")
                raise RuntimeError(output['message'])
        except subprocess.CalledProcessError as e:
            self.logger.error(f"R script execution failed: {e.stderr}")
            raise
        except Exception as e:
            self.logger.error(f"Other error in processing IDAT file: {str(e)}")
            self.logger.error(f"Full output: {output_lines}")
            raise

    def process_idat_from_gcs(self, pd_file_gcs_path: str, idat_folder_gcs_path: str) -> pd.DataFrame:
        self.logger.info(f"Processing IDAT files from GCS: {idat_folder_gcs_path}")
        self.logger.info(f"Using Sample Sheet from GCS: {pd_file_gcs_path}")

        # 移除 "gs://bucket-name/" 前綴
        bucket_name = idat_folder_gcs_path.split('/')[2]
        prefix = '/'.join(idat_folder_gcs_path.split('/')[3:])

        with tempfile.TemporaryDirectory() as temp_dir:
            idat_dir = Path(temp_dir) / "idat_files"
            idat_dir.mkdir(exist_ok=True)

            # 下載 Sample Sheet
            try:
                pd_file_content = self.gcs_storage.download_as_text_utf8(pd_file_gcs_path)
                pd_file_path = idat_dir / "Sample_Sheet.csv"
                with open(pd_file_path, 'w') as f:
                    f.write(pd_file_content)
                self.logger.info(f"Sample Sheet downloaded to {pd_file_path}")
            except Exception as e:
                self.logger.error(f"Failed to download Sample Sheet: {str(e)}")
                raise

            # 列出並下載 IDAT 文件
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blobs = bucket.list_blobs(prefix=prefix)

            total_files = sum(1 for blob in blobs if blob.name.endswith('.idat'))
            self.logger.info(f"Total IDAT files to download: {total_files}")

            downloaded_files = 0
            blobs = bucket.list_blobs(prefix=prefix)  # 重新獲取迭代器
            for blob in blobs:
                if blob.name.endswith('.idat'):
                    file_name = os.path.basename(blob.name)
                    file_path = idat_dir / file_name
                    try:
                        blob.download_to_filename(str(file_path))
                        downloaded_files += 1
                        self.logger.info(f"Downloaded {file_name} ({downloaded_files}/{total_files})")
                    except Exception as e:
                        self.logger.error(f"Failed to download {file_name}: {str(e)}")
                        raise

            if downloaded_files != total_files:
                error_msg = f"Expected to download {total_files} IDAT files, but only downloaded {downloaded_files}"
                self.logger.error(error_msg)
                raise RuntimeError(error_msg)

            self.logger.info(f"All IDAT files downloaded successfully. Total files: {total_files}")

            # 添加一個小延遲，確保所有文件都已完全寫入
            time.sleep(2)

            # 使用現有的 process_idat 方法處理下載的文件
            return self.process_idat(str(pd_file_path), str(idat_dir))

    def champ_df_postprocess(self, beta_table: pd.DataFrame) -> pd.DataFrame:
        '''
        後處理 CHAMP 輸出的 beta_table DataFrame

        :param beta_table: 從 CHAMP 腳本獲得的 beta_table DataFrame
        :return: 去除重複probe(重複的取平均)後的 DataFrame
        '''
        if 'probeID' not in beta_table.columns:
            raise ValueError("Expected 'probeID' column not found in the DataFrame")
        
        if beta_table.index.name != 'probeID':
            beta_table.set_index('probeID', inplace=True)
        
        grouped = beta_table.groupby(beta_table.index.str[:10])
        return grouped.mean()

    def save_processed_data(self, beta_table_rmdup: pd.DataFrame, batch_name: str) -> str:
        '''
        保存處理後的數據到 CSV 文件並更新數據庫
        
        :param beta_table_rmdup: 處理後的 DataFrame
        :param batch_name: 樣本名稱，用於生成文件名
        :return: 保存的文件的相對路徑
        '''
        gcs_path = f"data/processed_beta_table/{batch_name}_processed.csv"

        # 將 DataFrame 轉換為 CSV 格式的字符串
        csv_buffer = io.StringIO()
        beta_table_rmdup.to_csv(csv_buffer, index=True)
        csv_string = csv_buffer.getvalue()

        # 直接上傳字符串內容到 GCS
        gcs_url = self.gcs_storage.upload_string(csv_string, gcs_path)
        self.logger.info(f"Processed data saved to GCS: {gcs_url}")
        
        # Update database
        db = SessionLocal()
        try:
            # 獲取所有 sample_name
            sample_names = beta_table_rmdup.columns.tolist()
            
            # 批量查詢 sample_id
            samples = db.query(models.SampleData).filter(models.SampleData.sample_name.in_(sample_names)).all()
            
            # 創建 sample_name 到 sample 對象的映射
            sample_map = {sample.sample_name: sample for sample in samples}
            
            # 更新每個樣本的 processed_beta_table_path
            for sample_name in sample_names:
                sample = sample_map.get(sample_name)
                if sample:
                    sample.processed_beta_table_path = gcs_url
                else:
                    self.logger.warning(f"Sample with name {sample_name} not found in database")
            
            db.commit()
            self.logger.info(f"Updated processed_beta_table_path for {len(samples)} samples")
        except Exception as e:
            db.rollback()
            self.logger.error(f"Error updating database: {str(e)}")
        finally:
            db.close()
        
        return gcs_url


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process IDAT file")
    parser.add_argument("pd_file_path", help="Path to the Sample Sheet CSV file")
    parser.add_argument("idat_file_path", help="Path to the directory containing IDAT files")
    parser.add_argument("--batch_name", help="Name of the batch for output file", required=True)
    args = parser.parse_args()

    processor = IDATProcessor()

    try:
        # 示例用法
        # python app/services/idat_processor.py "D:/SideProject/EpiAging/SVD_test/raw/Sample_Sheet.csv" "D:/SideProject/EpiAging/SVD_test/raw" --batch_name our_all_samples
        result = processor.process_idat(args.pd_file_path, args.idat_file_path)
        if isinstance(result, pd.DataFrame):
            processed_result = processor.champ_df_postprocess(result)
            print("Processing completed. Sample of processed data:")
            print(processed_result.head())
            print(f"\nTotal number of items: {len(processed_result)}")
            
            relative_path = processor.save_processed_data(processed_result, args.batch_name)
            print(f"Processed data saved. Relative path: {relative_path}")
        else:
            print("Processing did not return a DataFrame.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
