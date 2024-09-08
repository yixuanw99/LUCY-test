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