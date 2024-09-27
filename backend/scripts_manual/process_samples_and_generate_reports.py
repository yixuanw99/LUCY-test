import sys
from pathlib import Path
import logging
from datetime import date
import pandas as pd
import io
import tempfile
import os

# 將專案根目錄添加到 Python 路徑
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from app.db.session import SessionLocal
from app.db import models
from app.services.report_generator import IdatReportGenerator, ProcessedDataReportGenerator
from app.db.models import SampleData
from app.core.config import settings
from app.services.gcs_storage import GCSStorage
from google.cloud import storage
from google.oauth2 import service_account
from dotenv import load_dotenv

# 加載 .env.development 文件
load_dotenv('.env.development')

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 還沒需要使用
def get_storage_client():
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    )
    return storage.Client(credentials=credentials)

# 還沒需要使用
def download_file_from_gcs(bucket_name, source_blob_name):
    """從 GCS 下載文件"""
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        blob.download_to_file(temp_file)
        temp_file_path = temp_file.name

    return temp_file_path

def upload_sample_data(pd_file_local_path):
    # 獲取目錄路徑
    directory_path = os.path.dirname(pd_file_local_path).replace(os.sep, '/')
    """從本地的CSV檔案導入樣本數據"""
    session = SessionLocal()
    try:
        df = pd.read_csv(pd_file_local_path)
        
        for _, row in df.iterrows():
            logger.info(f'Processing row: {row.to_dict()}')
            
            sentrix_id = str(row['Sentrix_ID'])
            sentrix_position = str(row['Sentrix_Position'])
            idat_file = f"{directory_path}/{sentrix_id}_{sentrix_position}_Grn.idat,{directory_path}/{sentrix_id}_{sentrix_position}_Red.idat"

            existing_sample = session.query(SampleData).filter_by(
                Sentrix_ID=sentrix_id,
                Sentrix_Position=sentrix_position
            ).first()

            if existing_sample:
                logger.warning(f"Sample already exists: {row['Sample_Name']}")
                continue

            new_sample = SampleData(
                sample_name=row['Sample_Name'],
                Sentrix_ID=sentrix_id,
                Sentrix_Position=sentrix_position,
                idat_file=idat_file
            )
            session.add(new_sample)

        session.commit()
        logger.info("All samples have been imported successfully.")
    except Exception as e:
        session.rollback()
        logger.error(f"An error occurred: {str(e)}")
    finally:
        session.close()

def upload_sample_data_from_gcs(pd_file_gcs_path):
    """從GCS的CSV檔案導入樣本數據"""
    gcs_storage = GCSStorage()
    session = SessionLocal()
    try:
        pd_file_content = gcs_storage.download_as_text_utf8(pd_file_gcs_path)
        df = pd.read_csv(io.StringIO(pd_file_content))
        
        for _, row in df.iterrows():
            logger.info(f'Processing row: {row.to_dict()}')
            
            sentrix_id = str(row['Sentrix_ID'])
            sentrix_position = str(row['Sentrix_Position'])
            idat_file = f"data/raw/run1/{sentrix_id}_{sentrix_position}_Grn.idat,data/raw/run1/{sentrix_id}_{sentrix_position}_Red.idat"

            existing_sample = session.query(SampleData).filter_by(
                Sentrix_ID=sentrix_id,
                Sentrix_Position=sentrix_position
            ).first()

            if existing_sample:
                logger.warning(f"Sample already exists: {row['Sample_Name']}")
                continue


            new_sample = SampleData(
                sample_name=row['Sample_Name'],
                Sentrix_ID=sentrix_id,
                Sentrix_Position=sentrix_position,
                idat_file=idat_file
            )
            session.add(new_sample)

        session.commit()
        logger.info("All samples have been imported successfully.")
    except Exception as e:
        session.rollback()
        logger.error(f"An error occurred: {str(e)}")
    finally:
        session.close()

def generate_reports(pd_file_local_path, idat_folder_local_path, batch_name):
    """生成報告"""
    db = SessionLocal()
    try:
        # TODO: 從數據庫中獲取樣本的年齡和性別信息
        # samples = db.query(models.SampleData).all()
        # metadata = {
        #     'age': [sample.user.birthday.year for sample in samples],
        #     'sex': [2 if sample.user.sex == 'F' else 1 for sample in samples]
        # }
        # metadata = {
        #     'age': [42, 42, 43, 43, 43, 28, 28, 28, 42, 42, 43, 43, 43, 28, 28, 28],
        #     'sex': [2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1]
        # }
        
        local_generator = IdatReportGenerator()
        local_generator.process_data(pd_file_local_path, idat_folder_local_path, batch_name)
        report_from_local = local_generator.generate_and_save_reports()
        logger.info(f"Generated and saved {len(report_from_local)} reports.")
    finally:
        db.close()

def generate_reports_from_local_betas(local_betas_path):
    """生成報告"""
    db = SessionLocal()
    try:
        # TODO: 從數據庫中獲取樣本的年齡和性別信息
        # samples = db.query(models.SampleData).all()
        # metadata = {
        #     'age': [sample.user.birthday.year for sample in samples],
        #     'sex': [2 if sample.user.sex == 'F' else 1 for sample in samples]
        # }
        # metadata = {
        #     'age': [42, 42, 43, 43, 43, 28, 28, 28, 42, 42, 43, 43, 43, 28, 28, 28],
        #     'sex': [2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1]
        # }
        
        local_betas_report_generator = ProcessedDataReportGenerator()
        local_betas_report_generator.process_data(local_betas_path)
        report_from_local = local_betas_report_generator.generate_and_save_reports()
        logger.info(f"Generated and saved {len(report_from_local)} reports.")
    finally:
        db.close()

def generate_reports_from_gcs(pd_file_gcs_path, idat_folder_gcs_path):
    """生成報告"""
    db = SessionLocal()
    try:
        # TODO: 從數據庫中獲取樣本的年齡和性別信息
        # samples = db.query(models.SampleData).all()
        # metadata = {
        #     'age': [sample.user.birthday.year for sample in samples],
        #     'sex': [2 if sample.user.sex == 'F' else 1 for sample in samples]
        # }
        metadata = {
            'age': [42, 42, 43, 43, 43, 28, 28, 28, 42, 42, 43, 43, 43, 28, 28, 28],
            'sex': [2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1]
        }
        
        gcs_generator = IdatReportGenerator()
        gcs_generator.process_data(pd_file_gcs_path, idat_folder_gcs_path)
        report_from_gcs = gcs_generator.generate_and_save_reports(metadata)
        logger.info(f"Generated and saved {len(report_from_gcs)} reports.")
    finally:
        db.close()

def main(pd_file_path, idat_folder_path, batch_name):
    """主函數，執行整個流程"""
    logger.info("Starting sample processing and report generation...")
    
    upload_sample_data(pd_file_path)
    # generate_reports(pd_file_path, idat_folder_path, batch_name)
    local_betas_path = project_root / 'data' / 'processed_beta_table' / 'GSE111631_2_processed.csv'
    generate_reports_from_local_betas(local_betas_path)
    
    logger.info("Sample processing and report generation completed.")

if __name__ == "__main__":
    # PD_FILE_GCS_PATH = "gs://lucy-data-storage/data/raw/run1/Sample_Sheet.csv"
    # IDAT_FOLDER_GCS_PATH = "gs://lucy-data-storage/data/raw/run1/"
    PD_FILE_PATH = project_root / "data" / "raw" / "GSE111631_2" / "Sample_Sheet.csv"
    IDAT_FOLDER_PATH = project_root / "data" / "raw" / "GSE111631_2"
    batch_name = "GSE111631_2"

    
    main(PD_FILE_PATH, IDAT_FOLDER_PATH, batch_name)