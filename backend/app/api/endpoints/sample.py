# backend/app/api/endpoints/sample.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.schemas import sample as sample_schema
from typing import List

router = APIRouter()

@router.get("/sample/{sample_id}", response_model=sample_schema.SampleData)
def get_sample(sample_id: str, db: Session = Depends(get_db)):
    sample = db.query(models.SampleData).filter(models.SampleData.sample_id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    return sample

@router.get("/samples", response_model=List[sample_schema.SampleData])
def get_all_samples(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    samples = db.query(models.SampleData).offset(skip).limit(limit).all()
    return samples

@router.post("/sample", response_model=sample_schema.SampleData)
def create_sample(sample: sample_schema.SampleDataCreate, db: Session = Depends(get_db)):
    db_sample = models.SampleData(**sample.dict())
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample