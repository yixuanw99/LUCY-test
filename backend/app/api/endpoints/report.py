# backend/app/api/endpoints/report.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.schemas import report as report_schema
from app.services import report_generator
from app.api.deps import get_current_active_user
from app.schemas.user import User
from typing import List

router = APIRouter()

@router.get("/report/{sample_id}", response_model=report_schema.Report)
def get_report(sample_id: str, db: Session = Depends(get_db)):
    report = db.query(models.Report).filter(models.Report.sample_id == sample_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.post("/report/{sample_id}", response_model=report_schema.Report)
def create_report(sample_id: str, db: Session = Depends(get_db)):
    existing_report = db.query(models.Report).filter(models.Report.sample_id == sample_id).first()
    if existing_report:
        raise HTTPException(status_code=400, detail="Report already exists for this sample")

    sample = db.query(models.SampleData).filter(models.SampleData.sample_id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    
    report_data = report_generator.generate_report(sample.idat_file)
    report = models.Report(sample_id=sample_id, **report_data)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

@router.get("/user/reports", response_model=List[report_schema.Report])
def get_user_reports(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    reports = db.query(models.Report).filter(models.Report.user_id == current_user.id).offset(skip).limit(limit).all()
    return reports

@router.get("/admin/reports", response_model=List[report_schema.Report])
def get_all_reports(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to access all reports")
    reports = db.query(models.Report).offset(skip).limit(limit).all()
    return reports