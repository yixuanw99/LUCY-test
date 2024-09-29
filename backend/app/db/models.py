# backend/app/db/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    order_ecid = Column(String(255))
    cdt = Column(DateTime(timezone=True))
    bio_age = Column(Float)
    pace_value = Column(Float)
    pace_pr = Column(Float)
    fitage = Column(Float)
    fitage_pr = Column(Float)
    vo2max = Column(Float)
    vo2max_pr = Column(Float)
    grip = Column(Float)
    grip_pr = Column(Float)
    gait = Column(Float)
    gait_pr = Column(Float)
    mentalhealth = Column(Float)
    mentalhealth_pr = Column(Float)
    cystatin = Column(Float)
    adm = Column(Float)
    timp = Column(Float)
    pai1 = Column(Float)
    packyrs = Column(Float)

class SampleData(Base):
    __tablename__ = "sample_data"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    sample_name = Column(String(255))
    Sentrix_ID = Column(String(12))
    Sentrix_Position = Column(String(6))
    idat_file = Column(String(255))
    processed_beta_table_path = Column(String(255), nullable=True)
    cell_proportion_path = Column(String(255), nullable=True)
    biolearn_output_path = Column(String(255), nullable=True)
    epigentl_output_path = Column(String(255), nullable=True)

# 初始化數據庫的函數
def init_db(engine):
    Base.metadata.create_all(engine)