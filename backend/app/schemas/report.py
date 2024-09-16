# backend/app/schemas/report.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

class ReportBase(BaseModel):
    user_id: int
    sample_id: int
    collection_date: date
    chro_age: float

class ReportCreate(ReportBase):
    user_id: int
    sample_id: int
    collection_date: date
    report_date: date
    bio_age: float
    chro_age: float
    pace_value: float
    pace_pr: int

class ReportUpdate(BaseModel):
    bio_age: Optional[float] = None
    chro_age: Optional[float] = None
    pace_value: Optional[float] = None
    pace_pr: Optional[int] = None

class Report(ReportBase):
    id: int
    user_id: int
    sample_id: int
    collection_date: date
    report_date: date
    bio_age: float
    chro_age: float
    pace_value: float
    pace_pr: int

    class Config:
        from_attributes = True

class ReportWithUser(Report):
    user: "User"

class ReportWithSample(Report):
    sample_data: "SampleData"

from .user import User
from .sample import SampleData

ReportWithUser.model_rebuild()
ReportWithSample.model_rebuild()
