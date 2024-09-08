# backend/app/schemas/report.py
from pydantic import BaseModel
from datetime import datetime

class ReportBase(BaseModel):
    title: str
    description: str | None = None

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True
