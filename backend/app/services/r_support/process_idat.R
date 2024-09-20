# R腳本 (process_idat.R)
# 從命令行參數獲取文件路徑
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) {
  stop("Usage: Rscript process_idat.R <pd_file_path> <idat_file_path>")
}

library(ChAMP)
library(jsonlite)

process_idat <- function(pd_file_path, idat_file_path) {
  tryCatch({
    # 檢查文件是否存在
    if (!file.exists(pd_file_path)) {
      stop(paste("Sample sheet file not found:", pd_file_path))
    }
    if (!dir.exists(idat_file_path)) {
      stop(paste("IDAT directory not found:", idat_file_path))
    }

    pd_file <- read.table(pd_file_path, header = TRUE, sep = ",")
    myDir <- idat_file_path
    myLoad <- champ.load(directory=myDir,arraytype="EPICv2")
    myNorm <- champ.norm(beta = myLoad$beta, arraytype = "EPICv2", cores = 3)
    
    # 將行名轉換為一個名為 'probeID' 的列
    myNorm_df <- as.data.frame(myNorm)
    # myNorm_df <- as.data.frame(myLoad$beta[1:1000, ])  # 只取前1000行以測試
    myNorm_df$probeID <- rownames(myNorm_df)
    
    # 將 'probeID' 列移到第一列
    myNorm_df <- myNorm_df[, c('probeID', setdiff(names(myNorm_df), 'probeID'))]

    # 按照 probeID 排序
    myNorm_df <- myNorm_df[order(myNorm_df$probeID), ]
    
    # 創建一個包含數據、行名和列名的列表
    result_list <- list(
      beta_table = myNorm_df,
      rownames = myNorm_df$probeID,
      colnames = colnames(myNorm_df)
    )

    # 將結果轉換為JSON並寫入標準輸出
    json_data <- toJSON(list(status = "success", data = result_list), auto_unbox = TRUE)
    cat(json_data)
  }, error = function(e) {
    # 錯誤處理
    error_json <- toJSON(list(status = "error", message = as.character(e)))
    cat(error_json)
  })
}

process_idat(args[1], args[2])