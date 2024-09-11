# app/services/epidish_cell_proportion.py
import pandas as pd
import logging
import os
import subprocess
import json
from dotenv import load_dotenv
from pathlib import Path

class EpiDISHProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.backend_root = Path(__file__).resolve().parents[2]
        env_path = self.backend_root / '.env.development'
        load_dotenv(dotenv_path=env_path)
        self.r_script_path = os.getenv('EPIDISH_R_SCRIPT_PATH')
        self.r_executable = os.getenv('R_EXECUTABLE')

    def run_epidish_with_csv(self, csv_file_path: str) -> pd.DataFrame:
        '''
        使用 R 的 EpiDISH 包處理 CSV 文件，並返回細胞比例的 DataFrame
        
        :param csv_file_path: 包含甲基化數據的 CSV 文件的路徑
        :return: EpiDISH 處理後的細胞比例 DataFrame
        '''
        self.logger.info(f"Processing CSV file with EpiDISH: {csv_file_path}")

        if not self.r_script_path:
            raise ValueError("EPIDISH_R_SCRIPT_PATH environment variable is not set")
        
        if not os.path.exists(self.r_script_path):
            raise FileNotFoundError(f"R script not found at {self.r_script_path}")
        
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"CSV file not found at {csv_file_path}")
                
        try:
            result = subprocess.run(
                [self.r_executable, self.r_script_path, csv_file_path],
                capture_output=True,
                text=True,
                check=True
            )

            output_lines = result.stdout.strip().split('\n')
            json_output = output_lines[-1]

            try:
                output = json.loads(json_output)
            except json.JSONDecodeError as json_error:
                self.logger.error(f"Failed to parse R script output as JSON: {json_error}")
                self.logger.error(f"R script output: {json_output}")
                raise
            
            if output['status'] == 'success':
                self.logger.info("EpiDISH processing completed successfully")
                self.logger.info(f"Output: {output}")
                
                cell_proportion_data = output['data']['cell_proportion']
                
                df = pd.DataFrame(cell_proportion_data)
                df.set_index('SampleID', inplace=True)
                
                return df
            
            else:
                self.logger.error(f"R script execution failed: {output.get('message', 'Unknown error')}")
                raise RuntimeError(output.get('message', 'Unknown error'))
        except subprocess.CalledProcessError as e:
            self.logger.error(f"R script execution failed: {e.stderr}")
            raise
        except Exception as e:
            self.logger.error(f"Other error in processing CSV file with EpiDISH: {str(e)}")
            raise

    def save_cell_proportions(self, cell_proportions: pd.DataFrame, batch_name: str) -> str:
        '''
        保存細胞比例數據到 CSV 文件
        
        :param cell_proportions: 細胞比例的 DataFrame
        :param batch_name: 樣本名稱，用於生成文件名
        :return: 保存的文件的相對路徑
        '''
        cell_proportions_dir = self.backend_root / 'data' / 'cell_proportions'
        output_file = cell_proportions_dir / f"{batch_name}_cell_proportions.csv"
        cell_proportions.to_csv(output_file, index=True)
        self.logger.info(f"Cell proportions saved to {output_file}")
        return output_file.relative_to(self.backend_root).as_posix()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process CSV file with EpiDISH")
    parser.add_argument("csv_file_path", help="Path to the CSV file containing methylation data")
    parser.add_argument("--batch_name", help="Name of the batch for output file", required=True)
    args = parser.parse_args()

    processor = EpiDISHProcessor()

    try:
        # 示例用法
        # python app/services/r_epidish_processor.py "data/processed_beta_table/our_all_samples_normed_processed.csv" --batch_name our_all_samples
        result = processor.run_epidish_with_csv(args.csv_file_path)
        if isinstance(result, pd.DataFrame):
            print("Processing completed. Sample of cell proportions:")
            print(result.head())
            print(f"\nTotal number of samples: {len(result)}")
            
            relative_path = processor.save_cell_proportions(result, args.batch_name)
            print(f"Cell proportions saved. Relative path: {relative_path}")
        else:
            print("Processing did not return a DataFrame.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
