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

# app/api/endpoints/report.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.services import report_generator

router = APIRouter()

@router.get("/report/{sample_id}")
def get_report(sample_id: str, db: Session = Depends(get_db)):
    report = db.query(models.Report).filter(models.Report.sample_id == sample_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.post("/report/{sample_id}")
def create_report(sample_id: str, db: Session = Depends(get_db)):
    sample = db.query(models.Sample).filter(models.Sample.sample_id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    
    report_data = report_generator.generate_report(sample.idat_file)
    report = models.Report(sample_id=sample_id, **report_data)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

# app/services/idat_processor.py
import numpy as np

def process_idat_file(file_path):
    # This is a placeholder for the actual IDAT file processing logic
    # You would implement the specific algorithm here
    # For demonstration, we're just returning random data
    return {
        "bio_age": np.random.uniform(50, 90),
        "chro_age": np.random.uniform(40, 80),
        "pace_value": np.random.uniform(0.7, 1.3),
        "pace_pr": np.random.randint(1, 100),
        # ... other calculated values ...
    }

# app/services/report_generator.py
from .idat_processor import process_idat_file
from datetime import date

def generate_report(idat_file):
    processed_data = process_idat_file(idat_file)
    
    return {
        "name": "測試用戶",  # This should be fetched from user data in a real scenario
        "collection_date": date.today(),
        "report_date": date.today(),
        "bio_age": processed_data["bio_age"],
        "chro_age": processed_data["chro_age"],
        "pace_value": processed_data["pace_value"],
        "pace_pr": processed_data["pace_pr"],
        # ... other fields ...
    }

# app/main.py
from fastapi import FastAPI
from app.api.endpoints import report, sample
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(report.router)
app.include_router(sample.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)