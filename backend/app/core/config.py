# backend/app/core/config.py

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# 確定當前環境
env = os.getenv("ENVIRONMENT", "development")

# 加載相應的 .env 文件
load_dotenv(f".env.{env}")

class Settings(BaseSettings):
    DATABASE_URL: str
    API_V1_STR: str
    PROJECT_NAME: str
    SECRET_KEY: str
    DEBUG: bool

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
