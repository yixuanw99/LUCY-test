# R腳本 (process_epigentl.R)
# 從命令行參數獲取文件路徑
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) {
  stop("Usage: Rscript process_epigentl.R <csv_file_path> <epigentl_source_functions_path>")
}

csv_file_path <- args[1]
epigentl_source_functions_path <- args[2]

print(paste("CSV file path:", csv_file_path))
print(paste("EpigenTL_SourceFunctions.R path:", epigentl_source_functions_path))

print(paste("Current working directory:", getwd()))

library(glmnet)
library(dplyr)
library(jsonlite)

# 檢查文件是否存在
if (!file.exists(epigentl_source_functions_path)) {
  stop(paste("EpigenTL_SourceFunctions.R not found at:", epigentl_source_functions_path))
}

# 加載EpigenTL函數和數據
tryCatch({
  # 加載 ExampleFiles.RData
  example_files_path <- file.path(dirname(epigentl_source_functions_path), "ExampleFiles.RData")
  if (file.exists(example_files_path)) {
    load(example_files_path)
    print("Successfully loaded ExampleFiles.RData")
  } else {
    stop(paste("ExampleFiles.RData not found at:", example_files_path))
  }

  # 加載 EpigenTL_SourceFunctions.R
  source(epigentl_source_functions_path)
  print("Successfully loaded EpigenTL_SourceFunctions.R")
  
  # 檢查必要的對象是否存在
  if(exists("C_Algorithms_GitHub")) {
    print("C_Algorithms_GitHub object found")
  } else {
    print("C_Algorithms_GitHub object not found")
  }
  
  if(exists("Saliva.2.Blood.DNAmBiomarkers")) {
    print("Saliva.2.Blood.DNAmBiomarkers function found")
  } else {
    print("Saliva.2.Blood.DNAmBiomarkers function not found")
  }
  
  # 列出加載的所有對象
  print("Loaded objects:")
  print(ls())
  
}, error = function(e) {
  print(paste("Error loading required files:", e$message))
  stop(e)
})

process_epigentl <- function(csv_file_path) {
  tryCatch({
    # 檢查文件是否存在
    if (!file.exists(csv_file_path)) {
      stop(paste("CSV file not found:", csv_file_path))
    }

    print(paste("Processing CSV file:", csv_file_path))

    # 讀取CSV文件
    beta_table <- read.csv(csv_file_path, header = TRUE, row.names = 1)

    # 轉置數據框，使樣本成為行，探針成為列
    beta_table_t <- t(beta_table)

    # 轉換為矩陣
    beta_matrix <- as.matrix(beta_table_t)

    print("Running Saliva.2.Blood.DNAmBiomarkers function...")

    # 運行Saliva.2.Blood.DNAmBiomarkers函數
    epigentl_results <- Saliva.2.Blood.DNAmBiomarkers(X = beta_matrix, 
                                                      method = "C", 
                                                      SalivaDNAmBiom = NULL)

    print("EpigenTL processing completed.")

    # 將結果轉換為數據框
    epigentl_df <- as.data.frame(epigentl_results)
    
    # 添加樣本ID列
    epigentl_df$SampleID <- rownames(epigentl_df)
    rownames(epigentl_df) <- NULL
    
    # 將SampleID列移到第一列
    epigentl_df <- epigentl_df[, c('SampleID', setdiff(names(epigentl_df), 'SampleID'))]

    # 創建一個包含數據、行名和列名的列表
    result_list <- list(
      epigentl_results = epigentl_df,
      rownames = epigentl_df$SampleID,
      colnames = colnames(epigentl_df)
    )

    # 將結果轉換為JSON並寫入標準輸出
    json_data <- toJSON(list(status = "success", data = result_list), auto_unbox = TRUE)
    cat(json_data)
  }, error = function(e) {
    # 錯誤處理
    print(paste("Error occurred:", e$message))
    error_json <- toJSON(list(status = "error", message = as.character(e)))
    cat(error_json)
  })
}

process_epigentl(csv_file_path)