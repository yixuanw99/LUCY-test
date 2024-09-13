# backend/app/db/models.py
from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy_utils.types.encrypted.encrypted_type import StringEncryptedType
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(StringEncryptedType(String, length=255, key='abc'), nullable=False)
    birthday = Column(Date)
    phone_number = Column(String(10))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # 關係
    reports = relationship("Report", back_populates="user")
    sample_data = relationship("SampleData", back_populates="user")

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    sample_id = Column(Integer, ForeignKey("sample_data.id"), nullable=False, unique=True, index=True)
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

    sample_data = relationship("SampleData", back_populates="report", uselist=False, foreign_keys=[sample_id])
    user = relationship("User", back_populates="reports")

class SampleData(Base):
    __tablename__ = "sample_data"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
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