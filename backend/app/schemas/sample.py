# backend/app/schemas/sample.py
from pydantic import BaseModel
from datetime import date

class SampleDataBase(BaseModel):
    sample_name: str
    Sentrix_ID: str
    Sentrix_Position: str
    idat_file: str


class SampleDataCreate(SampleDataBase):
    sample_name: str
    Sentrix_ID: str
    Sentrix_Position: str
    idat_file: str

class SampleData(SampleDataBase):
    id: int
    processed_beta_table_path: str
    cell_proportion_path: str

    class Config:
        from_attributes = True

class SampleDataInDB(SampleData):
    pass