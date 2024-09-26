# backend/app/db/models.py
from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("sample_data.id"), nullable=False, unique=True, index=True)
    collection_date = Column(Date)
    report_date = Column(Date)
    bio_age = Column(Float)
    chro_age = Column(Float)
    pace_value = Column(Float)
    pace_pr = Column(Integer)
    vo2max = Column(Float)
    grip = Column(Float)
    gait = Column(Float)
    cystatin = Column(Float)
    adm = Column(Float)
    timp = Column(Float)
    pai1 = Column(Float)
    packyrs = Column(Float)

    sample_data = relationship("SampleData", back_populates="report", uselist=False, foreign_keys=[order_id])

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

    report = relationship("Report", back_populates="sample_data", uselist=False)

# 初始化數據庫的函數
def init_db(engine):
    Base.metadata.create_all(engine)