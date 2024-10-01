# app/services/sa2bl_processor.py
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
import logging
from typing import Dict, Union

class SA2BLProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.backend_root = Path(__file__).resolve().parents[2]
        self.processed_beta_table_dir = self.backend_root / 'data' / 'processed_beta_table'
        self.epidish_data_dir = self.backend_root / 'data' / 'cell_proportions'
        self.resource_dir = self.backend_root / 'app' / 'resources'
        self.probes_file = self.resource_dir / 'model_probes' / 'DunedinPACE_probes.csv'
        self.lasso_model_file = self.resource_dir / 'adjust_models' / 'PACE20000_lasso_v1_EAA_7var.pkl'

    def read_model_probes(self, file_path: Union[str, Path] = None) -> pd.Series:
        """
        Read the model probes from a CSV file.
        
        :param file_path: Path to the CSV file containing model probes
        :return: Series of model probes
        """
        file_path = file_path or self.probes_file
        model_probes = pd.read_csv(file_path, header=None, names=['probeID'])
        return model_probes['probeID']

    def load_lasso_models(self, file_path: Union[str, Path] = None) -> Dict:
        """
        Load the LASSO models from a pickle file.
        
        :param file_path: Path to the pickle file containing LASSO models
        :return: Dictionary of LASSO models
        """
        file_path = file_path or self.lasso_model_file
        results_lasso = joblib.load(file_path)
        return {result['index']: result['model'] for result in results_lasso}

    def process_epidish_data(self, epidish_data: pd.DataFrame) -> pd.DataFrame:
        """
        Process EpiDISH data to calculate adjusted values.
        
        :param epidish_data: DataFrame containing EpiDISH data
        :return: Processed DataFrame
        """

        # Check for NaN values in input
        if epidish_data.isnull().values.any():
            self.logger.warning("NaN values found in input epidish_data")
            nan_counts = epidish_data.isnull().sum()
            self.logger.warning(f"NaN counts per column: {nan_counts}")

        sums = epidish_data.iloc[:, 2:8].sum(axis=1)
        new_df = pd.DataFrame(float(0), index=epidish_data.index, columns=epidish_data.columns)
        new_df.iloc[:, 2:8] = epidish_data.iloc[:, 2:8].div(sums.replace(0, np.inf), axis=0).fillna(0)
        samnsbl = epidish_data - new_df
        return samnsbl.iloc[:, [0, 1, 3, 4, 5, 6, 7]]

    def apply_lasso_correction(self, processed_data: pd.DataFrame, models: Dict) -> Dict:
        """
        Apply LASSO correction to processed data.
        
        :param processed_data: Processed EpiDISH data
        :param models: Dictionary of LASSO models
        :return: Dictionary of corrections
        """
        return {k: v.predict(processed_data) for k, v in models.items()}

    def adjust_methylation_data(self, methylation_data: pd.DataFrame, corrections: Dict) -> pd.DataFrame:
        """
        Adjust methylation data using calculated corrections.
        
        :param methylation_data: Original methylation data
        :param corrections: Calculated corrections
        :return: Adjusted methylation data
        """
        y_pred_samnbl = pd.DataFrame.from_dict(corrections, orient='index', columns=methylation_data.columns)
        adjusted_data = methylation_data - y_pred_samnbl
        return adjusted_data.dropna()
    
    def sa2bl(self, methylation_data: Union[str, Path, pd.DataFrame], 
              epidish_data: Union[str, Path, pd.DataFrame]) -> pd.DataFrame:
        """
        Process saliva-to-blood conversion from either CSV files or pandas DataFrames.
        
        :param methylation_data: Either a path to the CSV file, a Path object, or a DataFrame containing methylation data
        :param epidish_data: Either a path to the CSV file, a Path object, or a DataFrame containing EpiDISH data
        :return: Adjusted methylation data
        """
        self.logger.info("Processing sa2bl")
        
        # 處理 methylation_data
        if isinstance(methylation_data, (str, Path)):
            methylation_data = Path(methylation_data)
            self.logger.info(f"Reading methylation data from file: {methylation_data}")
            methylation_data_path = self.processed_beta_table_dir / methylation_data
            self.logger.info(f"methylation_data_path: {methylation_data_path}")
            methylation_data = pd.read_csv(methylation_data_path, index_col='probeID')
        elif not isinstance(methylation_data, pd.DataFrame):
            raise ValueError("methylation_data must be either a file path, a Path object, or a pandas DataFrame")

        # 處理 epidish_data
        if isinstance(epidish_data, (str, Path)):
            epidish_data = Path(epidish_data)
            self.logger.info(f"Reading EpiDISH data from file: {epidish_data}")
            epidish_data_path = self.processed_beta_table_dir / epidish_data  # 注意：現在使用相同的目錄
            epidish_data = pd.read_csv(epidish_data_path, index_col='SampleID')
        elif not isinstance(epidish_data, pd.DataFrame):
            raise ValueError("epidish_data must be either a file path, a Path object, or a pandas DataFrame")
        
        # 共同的處理邏輯
        model_probes = self.read_model_probes()
        lasso_models = self.load_lasso_models()
        
        methylation_data_filtered = methylation_data[methylation_data.index.isin(model_probes)]
        processed_epidish = self.process_epidish_data(epidish_data)

        self.logger.info(f"processed_epidish: {processed_epidish}")
        # Check for NaN values in epidish_data
        if processed_epidish.isnull().values.any():
            self.logger.error("NaN values found in processed_epidish")
            nan_counts = processed_epidish.isnull().sum()
            self.logger.error(f"NaN counts per column: {nan_counts}")

            # Find rows with NaN values
            rows_with_nan = processed_epidish[processed_epidish.isnull().any(axis=1)]
            self.logger.error("Rows containing NaN values:")
            self.logger.error(rows_with_nan)
            raise ValueError("processed_epidish contains NaN values. Please handle these before proceeding.")
        
        corrections = self.apply_lasso_correction(processed_epidish, lasso_models)
        adjusted_data = self.adjust_methylation_data(methylation_data_filtered, corrections)
        
        return adjusted_data

    def sa2bl_from_csv(self, beta_table_file_name: str, epidish_file_name: str) -> pd.DataFrame:
        """
        Process saliva-to-blood conversion from a CSV file.
        
        :param csv_file_name: Name of the CSV file in the processed_beta_table directory
        :return: Adjusted methylation data
        """
        self.logger.info(f"Processing sa2bl from beta table CSV: {beta_table_file_name}")
        
        beta_table_path = self.processed_beta_table_dir / beta_table_file_name
        methylation_data = pd.read_csv(beta_table_path, index_col='probeID')
        model_probes = self.read_model_probes()
        lasso_models = self.load_lasso_models()
        
        methylation_data_filtered = methylation_data[methylation_data.index.isin(model_probes)]
        
        epidish_data = pd.read_csv(self.epidish_data_dir / epidish_file_name, index_col='SampleID')
        processed_epidish = self.process_epidish_data(epidish_data)
        
        corrections = self.apply_lasso_correction(processed_epidish, lasso_models)
        adjusted_data = self.adjust_methylation_data(methylation_data_filtered, corrections)
        
        return adjusted_data

    def sa2bl_from_pd(self, methylation_data: pd.DataFrame, epidish_data: pd.DataFrame) -> pd.DataFrame:
        """
        Process saliva-to-blood conversion from pandas DataFrames.
        
        :param methylation_data: DataFrame containing methylation data
        :param epidish_data: DataFrame containing EpiDISH data
        :return: Adjusted methylation data
        """
        self.logger.info("Processing sa2bl from pandas DataFrames")
        
        model_probes = self.read_model_probes()
        lasso_models = self.load_lasso_models()
        
        methylation_data_filtered = methylation_data[methylation_data.index.isin(model_probes)]
        processed_epidish = self.process_epidish_data(epidish_data)
        
        corrections = self.apply_lasso_correction(processed_epidish, lasso_models)
        adjusted_data = self.adjust_methylation_data(methylation_data_filtered, corrections)
        
        return adjusted_data

if __name__ == "__main__":
    processor = SA2BLProcessor()
    
    # 示例用法 for sa2bl_from_csv
    result_from_csv = processor.sa2bl_from_csv("our_all_samples_processed.csv", "our_all_samples_cell_proportions.csv")
    print("Result from CSV:")
    print(result_from_csv.head())
    
    # 示例用法 for sa2bl_from_pd
    # 注意：這裏只是示例，實際運行可能需要較長時間
    # methylation_data = pd.read_csv('path/to/methylation_data.csv', index_col='probeID')
    # epidish_data = pd.read_csv('path/to/epidish_data.csv', index_col='SampleID')
    # result_from_pd = processor.sa2bl_from_pd(methylation_data, epidish_data)
    # print("Result from DataFrames:")
    # print(result_from_pd.head())

    # 如果要從頭開始處理 IDAT 文件，可以使用以下代碼（取消註釋後使用）
    # from app.services.idat_processor import IDATProcessor
    # from app.services.r_epidish_processor import EpiDISHProcessor
    # 
    # idat_processor = IDATProcessor()
    # epidish_processor = EpiDISHProcessor()
    # 
    # methylation_data = idat_processor.champ_df_postprocess(idat_processor.process_idat("D:/SideProject/EpiAging/SVD_test/raw/Sample_Sheet.csv", "D:/SideProject/EpiAging/SVD_test/raw"))
    # epidish_data = epidish_processor.run_epidish_with_csv("data/processed_beta_table/our_all_samples_processed.csv")
    # result_from_pd = processor.sa2bl_from_pd(methylation_data, epidish_data)
    # print("Result from full processing pipeline:")
    # print(result_from_pd.head())