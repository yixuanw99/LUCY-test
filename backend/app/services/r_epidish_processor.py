# app/services/epidish_cell_proportion.py
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

def run_epidish_with_csv(csv_file_path: str) -> pd.DataFrame:
    '''
    使用 R 的 EpiDISH 包處理 CSV 文件，並返回細胞比例的 DataFrame
    
    :param csv_file_path: 包含甲基化數據的 CSV 文件的路徑
    :return: EpiDISH 處理後的細胞比例 DataFrame
    '''
    logger.info(f"Processing CSV file with EpiDISH: {csv_file_path}")

    r_script_path = os.getenv('EPIDISH_R_SCRIPT_PATH')
    r_executable = os.getenv('R_EXECUTABLE')
    
    if not r_script_path:
        raise ValueError("EPIDISH_R_SCRIPT_PATH environment variable is not set")
    
    if not os.path.exists(r_script_path):
        raise FileNotFoundError(f"R script not found at {r_script_path}")
    
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found at {csv_file_path}")
            
    try:
        result = subprocess.run(
            [r_executable, r_script_path, csv_file_path],
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
            logger.error(f"R script output: {json_output}")
            raise
        
        if output['status'] == 'success':
            logger.info("EpiDISH processing completed successfully")
            logger.info(f"Output: {output}")
            
            # 從JSON中提取數據
            cell_proportion_data = output['data']['cell_proportion']
            
            # 創建DataFrame
            df = pd.DataFrame(cell_proportion_data)
            df.set_index('SampleID', inplace=True)
            
            return df
        
        else:
            logger.error(f"R script execution failed: {output.get('message', 'Unknown error')}")
            raise RuntimeError(output.get('message', 'Unknown error'))
    except subprocess.CalledProcessError as e:
        logger.error(f"R script execution failed: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Other error in processing CSV file with EpiDISH: {str(e)}")
        raise

def save_cell_proportions(cell_proportions: pd.DataFrame, batch_name: str) -> str:
    '''
    保存細胞比例數據到 CSV 文件
    
    :param cell_proportions: 細胞比例的 DataFrame
    :param batch_name: 樣本名稱，用於生成文件名
    :return: 保存的文件的相對路徑
    '''
    CELL_PROPORTIONS_DIR = BACKEND_ROOT / 'data' / 'cell_proportions'
    output_file = CELL_PROPORTIONS_DIR / f"{batch_name}_cell_proportions.csv"
    cell_proportions.to_csv(output_file, index=True)
    logging.info(f"Cell proportions saved to {output_file}")
    return output_file.relative_to(BACKEND_ROOT).as_posix()

if __name__ == "__main__":
    # demo usage
    # python app/services/r_epidish_processor.py "data/processed_beta_table/our_all_samples_normed_processed.csv"  --batch_name our_all_samples
    import argparse

    parser = argparse.ArgumentParser(description="Process CSV file with EpiDISH")
    parser.add_argument("csv_file_path", help="Path to the CSV file containing methylation data")
    parser.add_argument("--batch_name", help="Name of the batch for output file", required=True)
    args = parser.parse_args()

    try:
        result = run_epidish_with_csv(args.csv_file_path)
        if isinstance(result, pd.DataFrame):
            print("Processing completed. Sample of cell proportions:")
            print(result.head())
            print(f"\nTotal number of samples: {len(result)}")
            
            relative_path = save_cell_proportions(result, args.batch_name)
            print(f"Cell proportions saved. Relative path: {relative_path}")
        else:
            print("Processing did not return a DataFrame.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
