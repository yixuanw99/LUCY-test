# backend/init_db.py:
from app.db.base import engine
from app.db.models import Base, init_db

if __name__ == "__main__":
    init_db(engine)
    print("Database tables created.")