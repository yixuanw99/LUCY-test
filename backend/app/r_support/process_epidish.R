# R腳本 (process_epidish.R)
# 從命令行參數獲取文件路徑
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) {
  stop("Usage: Rscript process_epidish.R <csv_file_path>")
}

library(EpiDISH)
library(jsonlite)

process_epidish <- function(csv_file_path) {
  tryCatch({
    # 檢查文件是否存在
    if (!file.exists(csv_file_path)) {
      stop(paste("CSV file not found:", csv_file_path))
    }

    # 读取CSV文件
    data <- read.table(csv_file_path, header = TRUE, sep = ",")

    # 将probeID列的值设置为行名
    rownames(data) <- data$probeID
    # 删除原始的probeID列
    data <- data[, -1]

    data(centEpiFibIC.m)
    data(centBloodSub.m)
    cell_proportion <- hepidish(beta.m = data, ref1.m = centEpiFibIC.m, ref2.m = centBloodSub.m[,c(1:6)], h.CT.idx = 3, method = 'RPC')

    # 將結果轉換為數據框
    cell_proportion_df <- as.data.frame(cell_proportion)
    
    # 添加行名為新的列
    cell_proportion_df$SampleID <- rownames(cell_proportion_df)
    rownames(cell_proportion_df) <- NULL # 删除行名避免JSON存出"_row"
    
    # 將 SampleID 列移到第一列
    cell_proportion_df <- cell_proportion_df[, c('SampleID', setdiff(names(cell_proportion_df), 'SampleID'))]

    # 創建一個包含數據、行名和列名的列表
    result_list <- list(
      cell_proportion = cell_proportion_df,
      rownames = cell_proportion_df$SampleID,
      colnames = colnames(cell_proportion_df)
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

process_epidish(args[1])