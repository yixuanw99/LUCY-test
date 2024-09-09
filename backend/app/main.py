from fastapi import FastAPI
from app.api.endpoints import report, sample
from app.core.config import settings
import os
from app.db.base import Base
from app.db.session import engine

print(f"Current environment: {os.getenv('ENVIRONMENT', 'development')}")
print(f"Database URL: {settings.DATABASE_URL}")
print(f"Debug mode: {settings.DEBUG}")

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(report.router)
app.include_router(sample.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
