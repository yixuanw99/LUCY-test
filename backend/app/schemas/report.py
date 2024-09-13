# backend/app/schemas/report.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

class ReportBase(BaseModel):
    user_id: int
    sample_id: int
    collection_date: date
    report_date: date
    bio_age: float
    chro_age: float
    pace_value: float
    pace_pr: int

class ReportCreate(ReportBase):
    acm_horvath_risk: float
    cvd_horvath_risk: float
    dm_horvath_risk: float
    ad_horvath_risk: float
    cancer_horvath_risk: float
    acm_pace_risk: float
    cvd_pace_risk: float
    dm_pace_risk: float
    ad_pace_risk: float
    cancer_pace_risk: float

class ReportUpdate(BaseModel):
    bio_age: Optional[float] = None
    chro_age: Optional[float] = None
    pace_value: Optional[float] = None
    pace_pr: Optional[int] = None
    acm_horvath_risk: Optional[float] = None
    cvd_horvath_risk: Optional[float] = None
    dm_horvath_risk: Optional[float] = None
    ad_horvath_risk: Optional[float] = None
    cancer_horvath_risk: Optional[float] = None
    acm_pace_risk: Optional[float] = None
    cvd_pace_risk: Optional[float] = None
    dm_pace_risk: Optional[float] = None
    ad_pace_risk: Optional[float] = None
    cancer_pace_risk: Optional[float] = None

class Report(ReportBase):
    id: int
    acm_horvath_risk: float
    cvd_horvath_risk: float
    dm_horvath_risk: float
    ad_horvath_risk: float
    cancer_horvath_risk: float
    acm_pace_risk: float
    cvd_pace_risk: float
    dm_pace_risk: float
    ad_pace_risk: float
    cancer_pace_risk: float

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
