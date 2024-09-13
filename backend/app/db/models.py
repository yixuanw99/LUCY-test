# backend/app/db/models.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    birthday = Column(Date)
    phone_number = Column(String(10))
    
    # 關係
    reports = relationship("Report", back_populates="user")
    sample_data = relationship("SampleData", back_populates="user")

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    sample_id = Column(String(30), ForeignKey("sample_data.sample_id"), unique=True)
    collection_date = Column(Date)
    report_date = Column(Date)
    bio_age = Column(Float)
    chro_age = Column(Float)
    pace_value = Column(Float)
    pace_pr = Column(Integer)
    
    # Disease risks
    acm_horvath_risk = Column(Float) # acm = all cause mortality
    cvd_horvath_risk = Column(Float) # cvd = cardiovascular disease
    dm_horvath_risk = Column(Float) # dm = diabetes mellitus
    ad_horvath_risk = Column(Float) # ad = alzheimer's disease
    cancer_horvath_risk = Column(Float) # cancer
    acm_pace_risk = Column(Float)
    cvd_pace_risk = Column(Float)
    dm_pace_risk = Column(Float)
    ad_pace_risk = Column(Float)
    cancer_pace_risk = Column(Float)

    sample_data = relationship("SampleData", back_populates="report", uselist=False)
    user = relationship("User", back_populates="reports")

class SampleData(Base):
    __tablename__ = "sample_data"

    id = Column(Integer, primary_key=True)
    sample_id = Column(String(30), unique=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    report_id = Column(Integer, ForeignKey('reports.id'), nullable=False)
    Sentrix_ID = Column(String(12))
    Sentrix_Position = Column(String(6))
    idat_file = Column(String(255))
    processed_beta_table_path = Column(String(255))
    cell_proportion_path = Column(String(255))

    report = relationship("Report", back_populates="sample_data", uselist=False)
    user = relationship("User", back_populates="sample_data")

# 初始化數據庫的函數
def init_db(engine):
    Base.metadata.create_all(engine)