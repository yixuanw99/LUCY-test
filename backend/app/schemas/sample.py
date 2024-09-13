# backend/app/schemas/sample.py
from pydantic import BaseModel
from datetime import date

class SampleDataBase(BaseModel):
    sample_id: str
    user_id: int
    Sentrix_ID: str
    Sentrix_Position: str
    idat_file: str
    processed_beta_table_path: str
    cell_proportion_path: str

class SampleDataCreate(SampleDataBase):
    pass

class SampleData(SampleDataBase):
    id: int
    report_id: int | None = None

    class Config:
        from_attributes = True

class SampleDataInDB(SampleData):
    pass