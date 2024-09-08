# app/db/models.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(String, ForeignKey("samples.sample_id"), unique=True)
    name = Column(String)
    collection_date = Column(Date)
    report_date = Column(Date)
    bio_age = Column(Float)
    chro_age = Column(Float)
    pace_value = Column(Float)
    pace_pr = Column(Integer)
    diff_age = Column(Float)
    older_younger = Column(String)
    older_younger_comment = Column(String)
    
    # Disease risks
    allcausedead_higher = Column(Integer)
    heartdisease_higher = Column(Integer)
    diabetes_higher = Column(Integer)
    dementia_higher = Column(Integer)
    cancer_higher = Column(Integer)
    allcausedead_whenyoung1 = Column(Integer)
    heartdisease_whenyoung1 = Column(Integer)
    diabetes_whenyoung1 = Column(Integer)
    dementia_whenyoung1 = Column(Integer)
    cancer_whenyoung1 = Column(Integer)

    sample = relationship("Sample", back_populates="report")

class Sample(Base):
    __tablename__ = "samples"

    sample_id = Column(String, primary_key=True, index=True)
    idat_file = Column(String)

    report = relationship("Report", back_populates="sample", uselist=False)
    