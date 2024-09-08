# backend/app/core/config.py

import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # 設置默認值
    DATABASE_URL: str = "mysql://user:password@localhost:3306/lucy_db"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LUCY-Test"
    SECRET_KEY: str = "defaultsecret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BACKEND_CORS_ORIGINS: list = ["http://localhost:8080", "http://localhost:3000"]
    DEBUG: bool = False
    RELOAD: bool = False
    
    class Config:
        env_file = f".env.{os.getenv('ENVIRONMENT', 'development')}"

settings = Settings()