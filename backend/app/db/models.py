# backend/app/db/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    order_ecid = Column(String(255))
    gender = Column(Boolean, nullable=True)  # {False: female, True: male, None: unknown or other}
    age = Column(Float)
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
    fitage_fig_path = Column(String(255))
    vo2max_fig_path = Column(String(255))
    grip_fig_path = Column(String(255))
    gait_fig_path = Column(String(255))
    mentalhealth_fig_path = Column(String(255))
    cystatin_fig_path = Column(String(255))
    adm_fig_path = Column(String(255))
    timp_fig_path = Column(String(255))
    pai1_fig_path = Column(String(255))
    packyrs_fig_path = Column(String(255))

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