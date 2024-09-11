# app/services/sa2bl_processor.py
import pandas as pd
import joblib
import sys
from pathlib import Path
import logging
from typing import Dict, Union
sys.path.append(str(Path(__file__).resolve().parents[2]))
# from .idat_processor import process_idat, champ_df_postprocess
from app.services.idat_processor import process_idat, champ_df_postprocess
# from .r_epidish_processor import run_epidish_with_csv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set project root directory
BACKEND_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_CSV_DIR = BACKEND_ROOT / 'data' / 'processed_csv'
EPIDHSI_DATA_DIR = BACKEND_ROOT / 'data' / 'cell_proportions'
RESOURCE_DIR = BACKEND_ROOT / 'data' / 'biomarker_resource'
PROBES_FILE = RESOURCE_DIR / 'model_probes' / 'DunedinPACE_probes.csv'
LASSO_MODEL_FILE = RESOURCE_DIR/ 'adjust_models' / 'PACE20000_lasso_v1_EAA_7var.pkl'

def read_model_probes(file_path: Union[str, Path] = PROBES_FILE) -> pd.Series:
    """
    Read the model probes from a CSV file.
    
    :param file_path: Path to the CSV file containing model probes
    :return: Series of model probes
    """
    model_probes = pd.read_csv(file_path, header=None, names=['probeID'])
    return model_probes['probeID']

def load_lasso_models(file_path: Union[str, Path] = LASSO_MODEL_FILE) -> Dict:
    """
    Load the LASSO models from a pickle file.
    
    :param file_path: Path to the pickle file containing LASSO models
    :return: Dictionary of LASSO models
    """
    results_lasso = joblib.load(file_path)
    return {result['index']: result['model'] for result in results_lasso}

def process_epidish_data(epidish_data: pd.DataFrame) -> pd.DataFrame:
    """
    Process EpiDISH data to calculate adjusted values.
    
    :param epidish_data: DataFrame containing EpiDISH data
    :return: Processed DataFrame
    """
    sums = epidish_data.iloc[:, 2:8].sum(axis=1)
    new_df = pd.DataFrame(float(0), index=epidish_data.index, columns=epidish_data.columns)
    new_df.iloc[:, 2:8] = epidish_data.iloc[:, 2:8].div(sums, axis=0)
    samnsbl = epidish_data - new_df
    return samnsbl.iloc[:, [0, 1, 3, 4, 5, 6, 7]]

def apply_lasso_correction(processed_data: pd.DataFrame, models: Dict) -> Dict:
    """
    Apply LASSO correction to processed data.
    
    :param processed_data: Processed EpiDISH data
    :param models: Dictionary of LASSO models
    :return: Dictionary of corrections
    """
    return {k: v.predict(processed_data) for k, v in models.items()}

def adjust_methylation_data(methylation_data: pd.DataFrame, corrections: Dict) -> pd.DataFrame:
    """
    Adjust methylation data using calculated corrections.
    
    :param methylation_data: Original methylation data
    :param corrections: Calculated corrections
    :return: Adjusted methylation data
    """
    y_pred_samnbl = pd.DataFrame.from_dict(corrections, orient='index', columns=methylation_data.columns)
    adjusted_data = methylation_data - y_pred_samnbl
    return adjusted_data.dropna()

def sa2bl_from_csv(beta_table_file_name: str, epidish_file_name: str) -> pd.DataFrame:
    """
    Process saliva-to-blood conversion from a CSV file.
    
    :param csv_file_name: Name of the CSV file in the processed_csv directory
    :return: Adjusted methylation data
    """
    logger.info(f"Processing sa2bl from bata table CSV: {beta_table_file_name}")
    
    # Load necessary data
    beta_table_path = PROCESSED_CSV_DIR / beta_table_file_name
    methylation_data = pd.read_csv(beta_table_path, index_col='probeID')
    model_probes = read_model_probes()
    lasso_models = load_lasso_models()
    
    # Process data
    methylation_data_filtered = methylation_data[methylation_data.index.isin(model_probes)]
    
    # Assuming EpiDISH data is available, you might need to adjust this part
    epidish_data = pd.read_csv(EPIDHSI_DATA_DIR / epidish_file_name, index_col='SampleID')
    processed_epidish = process_epidish_data(epidish_data)
    
    corrections = apply_lasso_correction(processed_epidish, lasso_models)
    adjusted_data = adjust_methylation_data(methylation_data_filtered, corrections)
    
    return adjusted_data

def sa2bl_from_pd(methylation_data: pd.DataFrame, epidish_data: pd.DataFrame) -> pd.DataFrame:
    """
    Process saliva-to-blood conversion from pandas DataFrames.
    
    :param methylation_data: DataFrame containing methylation data
    :param epidish_data: DataFrame containing EpiDISH data
    :return: Adjusted methylation data
    """
    logger.info("Processing sa2bl from pandas DataFrames")
    
    # Load necessary data
    model_probes = read_model_probes()
    lasso_models = load_lasso_models()
    
    # Process data
    methylation_data_filtered = methylation_data[methylation_data.index.isin(model_probes)]
    processed_epidish = process_epidish_data(epidish_data)
    
    corrections = apply_lasso_correction(processed_epidish, lasso_models)
    adjusted_data = adjust_methylation_data(methylation_data_filtered, corrections)
    
    return adjusted_data

if __name__ == "__main__":
    # Example usage
    result_from_csv = sa2bl_from_csv("our_all_samples_normed_processed.csv", "our_all_samples_cell_proportions.csv")
    print("Result from CSV:")
    print(result_from_csv.head())
    
    # # For sa2bl_from_pd, you would need to provide the DataFrames directly
    # methylation_data = pd.read_csv('backend/data/processed_csv/our_all_samples_normed_processed.csv', index_col='probeID')
    # result_from_pd = sa2bl_from_pd(methylation_data, run_epidish_with_csv("backend/data/processed_csv/our_all_samples_normed_processed.csv"))
    
    # # 下面這行從頭跑，需要跑很久，所以還沒有測試
    # # result_from_pd = sa2bl_from_pd(champ_df_postprocess(process_idat("D:/SideProject/EpiAging/SVD_test/raw/Sample_Sheet.csv", "D:/SideProject/EpiAging/SVD_test/raw")), run_epidish_with_csv("data/processed_csv/our_all_samples_normed_processed.csv"))
    # print("Result from DataFrames:")
    # print(result_from_pd.head())