# 使用官方 Python 運行時作為父鏡像
FROM python:3.10

# 設置工作目錄
WORKDIR /app

# 複製 requirements.txt 文件
COPY requirements.txt .

# 安裝 R
# RUN apt-get update && apt-get install -y \
#     r-base \
#     && rm -rf /var/lib/apt/lists/*

# # 安裝 R 包
# RUN R -e "install.packages('BiocManager', repos='http://cran.rstudio.com/')"
# RUN R -e "BiocManager::install('EpiDISH')"
# RUN R -e "install.packages(c('jsonlite', 'glmnet', 'dplyr', 'devtools'), repos='http://cran.rstudio.com/')"
# RUN R -e "devtools::install_github('YuanTian1991/ChAMP')"
# RUN R -e "devtools::install_github('YuanTian1991/ChAMPdata')"

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程序代碼
COPY . .

# 設置環境變量
ENV ENVIRONMENT=production
ENV DATABASE_URL=${DATABASE_URL}
ENV GCS_BUCKET_NAME=${GCS_BUCKET_NAME}
ENV API_V1_STR=/api/v1
ENV PROJECT_NAME=LUCY-Test-Prod
# ENV CHAMP_R_SCRIPT_PATH=/app/app/services/r_support/process_idat.R
# ENV EPIDISH_R_SCRIPT_PATH=/app/app/services/r_support/process_epidish.R
# ENV EPIGENTL_R_SCRIPT_PATH=/app/app/services/r_support/process_epigentl.R
# ENV R_EXECUTABLE=/usr/bin/Rscript

# 暴露端口
EXPOSE 8000

# 運行應用程序
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
