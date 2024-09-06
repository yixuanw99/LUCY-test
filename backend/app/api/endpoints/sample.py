from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter()

@router.get("/sample/{sample_id}")
def get_sample(sample_id: str, db: Session = Depends(get_db)):
    # Implement get sample logic
    pass