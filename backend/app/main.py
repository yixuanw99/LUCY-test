from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.api.endpoints import report, sample, user
from app.core.config import settings
import os
import base64
import tempfile
import atexit
from app.db.base import Base
from app.db.session import engine

import logging

# 全局變量來存儲臨時文件的路徑
temp_cred_file = None

def setup_google_credentials():
    global temp_cred_file
    if 'GOOGLE_APPLICATION_CREDENTIALS_CONTENT' in os.environ:
        # 解碼 base64 內容
        creds_content = base64.b64decode(os.environ['GOOGLE_APPLICATION_CREDENTIALS_CONTENT']).decode('utf-8')
        
        # 創建一個臨時文件
        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, 'w') as tmp:
            # 將內容寫入臨時文件
            tmp.write(creds_content)
        
        # 設置 GOOGLE_APPLICATION_CREDENTIALS 環境變量指向這個臨時文件
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
        temp_cred_file = path

def cleanup_temp_file():
    global temp_cred_file
    if temp_cred_file and os.path.exists(temp_cred_file):
        os.remove(temp_cred_file)

# 在應用程序啟動時調用
setup_google_credentials()

# 註冊清理函數，在應用程序退出時執行
atexit.register(cleanup_temp_file)

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


print(f"Current environment: {os.getenv('ENVIRONMENT', 'development')}")
print(f"Database URL: {settings.DATABASE_URL}")
print(f"Debug mode: {settings.DEBUG}")

if settings.ENVIRONMENT == "development":
    Base.metadata.create_all(bind=engine)
    logger.info(f"Tables created: {', '.join(Base.metadata.tables.keys())}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="developed by yixuanw99",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8080", "http://localhost:8080"],  # 允許的前端源
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有方法
    allow_headers=["*"],  # 允許所有頭
)

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_json():
    return JSONResponse(get_openapi(
        title="Your API",
        version="1.0.0",
        routes=app.routes,
    ))

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error occurred"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"}
    )


app.include_router(report.router)
app.include_router(sample.router)
app.include_router(user.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
