# app/services/idat_processor.py
import pandas as pd
import logging
import os
import subprocess
import json
from dotenv import load_dotenv
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set project root directory
BACKEND_ROOT = Path(__file__).resolve().parents[2]
env_path = BACKEND_ROOT / '.env.development'
load_dotenv(dotenv_path=env_path)


def process_idat(pd_file_path, idat_file_path) -> pd.DataFrame:
    '''
    使用 R 腳本處理 IDAT 文件，並返回處理後的 DataFrame
    
    :param pd_file_path: Sample Sheet CSV 文件的路徑
    :param idat_file_path: 包含 IDAT 文件的目錄的路徑
    :return: ChAMP處理後的 DataFrame
    '''
    logger.info(f"Processing IDAT file: {idat_file_path}")
    logger.info(f"Using Sample Sheet: {pd_file_path}")

    r_script_path = os.getenv('CHAMP_R_SCRIPT_PATH')
    r_executable = os.getenv('R_EXECUTABLE')
    
    if not r_script_path:
        raise ValueError("R_SCRIPT_PATH environment variable is not set")
    
    if not os.path.exists(r_script_path):
        raise FileNotFoundError(f"R script not found at {r_script_path}")
    
    if not os.path.exists(pd_file_path):
        raise FileNotFoundError(f"Sample Sheet not found at {pd_file_path}")
    
    if not os.path.exists(idat_file_path):
        raise FileNotFoundError(f"IDAT directory not found at {idat_file_path}")
            
    try:
        result = subprocess.run(
            [r_executable, r_script_path, pd_file_path, idat_file_path],
            capture_output=True,
            text=True,
            check=True
        )

        # 分離標準輸出中的JSON數據
        output_lines = result.stdout.strip().split('\n')
        json_output = output_lines[-1]  # 假設JSON總是最後一行

        try:
            output = json.loads(json_output)
        except json.JSONDecodeError as json_error:
            logger.error(f"Failed to parse R script output as JSON: {json_error}")
            logger.error(f"R script output: {output_lines}")
            raise
        
        if output['status'] == 'success':
            logger.info("IDAT processing completed successfully")
            
            # 從JSON中提取數據、行名和列名
            beta_table = output['data']['beta_table']
            rownames = output['data']['rownames']
            colnames = output['data']['colnames']
            
            # 創建DataFrame
            df = pd.DataFrame(beta_table, index=rownames, columns=colnames)
            
            return df
        
        else:
            logger.error(f"R script execution failed: {output['message']}")
            raise RuntimeError(output['message'])
    except subprocess.CalledProcessError as e:
        logger.error(f"R script execution failed: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Other error in processing IDAT file: {str(e)}")
        logger.error(f"Full output: {output_lines}")
        raise

def champ_df_postprocess(beta_table: pd.DataFrame) -> pd.DataFrame:
    '''
    後處理 CHAMP 輸出的 beta_table DataFrame

    :param beta_table: 從 CHAMP 腳本獲得的 beta_table DataFrame
    :return: 去除重複probe(重複的取平均)後的 DataFrame
    '''
    # 確保 'probeID' 列存在
    if 'probeID' not in beta_table.columns:
        raise ValueError("Expected 'probeID' column not found in the DataFrame")
    
    # 設置 'probeID' 為索引（如果還不是）
    if beta_table.index.name != 'probeID':
        beta_table.set_index('probeID', inplace=True)
    
    # 根據 probeID 的前 10 個字符進行分組，並計算平均值
    grouped = beta_table.groupby(beta_table.index.str[:10])
    result = grouped.mean()
    
    return result

def save_processed_data(beta_table_rmdup: pd.DataFrame, batch_name: str) -> str:
    '''
    保存處理後的數據到 CSV 文件
    
    :param beta_table_rmdup: 處理後的 DataFrame
    :param batch_name: 樣本名稱，用於生成文件名
    :return: 保存的文件的相對路徑
    '''
    PROCESSED_CSV_DIR = BACKEND_ROOT / 'data' / 'processed_csv'
    output_file = PROCESSED_CSV_DIR / f"{batch_name}_processed.csv"
    beta_table_rmdup.to_csv(output_file, index=True)
    logging.info(f"Processed data saved to {output_file}")
    return output_file.relative_to(BACKEND_ROOT).as_posix()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process IDAT file")
    parser.add_argument("pd_file_path", help="Path to the Sample Sheet CSV file")
    parser.add_argument("idat_file_path", help="Path to the directory containing IDAT files")
    parser.add_argument("--batch_name", help="Name of the batch for output file", required=True)
    args = parser.parse_args()

    try:
        # demo usage
        # python app/services/idat_processor.py "D:/SideProject/EpiAging/SVD_test/raw/Sample_Sheet.csv" "D:/SideProject/EpiAging/SVD_test/raw" --batch_name our_all_samples
        result = process_idat(args.pd_file_path, args.idat_file_path)
        if isinstance(result, pd.DataFrame):
            processed_result = champ_df_postprocess(result)
            print("Processing completed. Sample of processed data:")
            print(processed_result.head())
            print(f"\nTotal number of items: {len(processed_result)}")
            
            relative_path = save_processed_data(processed_result, args.batch_name)
            print(f"Processed data saved. Relative path: {relative_path}")
            # 這裡您可以將 relative_path 保存到數據庫中
        else:
            print("Processing did not return a DataFrame.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")