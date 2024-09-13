# backend/app/api/endpoints/test_db.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User

router = APIRouter()

@router.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    user_count = db.query(User).count()
    return {"message": "Database connection successful", "user_count": user_count}