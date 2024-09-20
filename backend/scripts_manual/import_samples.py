# backend/scripts_manual/import_samples.py
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import sys
import os

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

# print(f"Project root: {project_root}")
# print(f"Python path: {sys.path}")
# print(f"Current working directory: {os.getcwd()}")

from app.db.models import SampleData, User
from app.core.config import settings
import logging



# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 創建數據庫連接
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_user_id(session, username):
    user = session.query(User).filter(User.name == username).first()
    if not user:
        logger.warning(f"User not found: {username}")
        return None
    return user.id

def import_samples(csv_file_path):
    session = SessionLocal()
    try:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = get_user_id(session, row['customer'])
                if not user_id:
                    logger.error(f"Skipping row due to missing user: {row}")
                    continue

                sentrix_id = row['Sentrix_ID']
                sentrix_position = row['Sentrix_Position']
                idat_file = f"data/raw/run1/{sentrix_id}_{sentrix_position}_Grn.idat,data/raw/run1/{sentrix_id}_{sentrix_position}_Red.idat"

                # 檢查是否已存在相同的樣本
                existing_sample = session.query(SampleData).filter_by(
                    user_id=user_id,
                    Sentrix_ID=sentrix_id,
                    Sentrix_Position=sentrix_position
                ).first()

                if existing_sample:
                    logger.warning(f"Sample already exists: {row['Sample_Name']}")
                    continue

                new_sample = SampleData(
                    user_id=user_id,
                    sample_name=row['Sample_Name'],
                    Sentrix_ID=sentrix_id,
                    Sentrix_Position=sentrix_position,
                    idat_file=idat_file
                )
                session.add(new_sample)
                logger.info(f"Added sample: {row['Sample_Name']}")

        session.commit()
        logger.info("All samples have been imported successfully.")
    except Exception as e:
        session.rollback()
        logger.error(f"An error occurred: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    csv_file_path = project_root / "data" / "raw" / "run1" / "Sample_Sheet.csv"
    print(f"Importing samples from {csv_file_path}")
    import_samples(csv_file_path)