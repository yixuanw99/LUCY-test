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
    acm_horvath_risk = Column(Integer) # acm = all cause mortality
    cvd_horvath_risk = Column(Integer) # cvd = cardiovascular disease
    dm_horvath_risk = Column(Integer) # dm = diabetes mellitus
    ad_horvath_risk = Column(Integer) # ad = alzheimer's disease
    cancer_horvath_risk = Column(Integer) # cancer
    acm_pace_risk = Column(Integer)
    cvd_pace_risk = Column(Integer)
    dm_pace_risk = Column(Integer)
    ad_pace_risk = Column(Integer)
    cancer_pace_risk = Column(Integer)

    sample = relationship("Sample", back_populates="report")

class Sample(Base):
    __tablename__ = "samples"

    sample_id = Column(String, primary_key=True, index=True)
    idat_file = Column(String)

    report = relationship("Report", back_populates="sample", uselist=False)
    