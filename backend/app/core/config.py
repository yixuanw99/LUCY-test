# backend/app/core/config.py
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from typing import List

# 確定當前環境
env = os.getenv("ENVIRONMENT", "development")

# 加載相應的 .env 文件
env_file = f".env.{env}"
load_dotenv(env_file)

class Settings(BaseSettings):
    ENVIRONMENT: str
    DATABASE_URL: str
    GCS_BUCKET_NAME: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    API_V1_STR: str
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[str]
    LOG_LEVEL: str
    CHAMP_R_SCRIPT_PATH: str
    EPIDISH_R_SCRIPT_PATH: str
    EPIGENTL_R_SCRIPT_PATH: str
    R_EXECUTABLE: str
    DEBUG: bool = False

    # Authentication settings (deps.py) 還沒做
    # SECRET_KEY: str
    # ALGORITHM: str
    # ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=env_file)

settings = Settings()