# app/services/biolearn_processor.py
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import List, Dict, Union
from biolearn.model_gallery import ModelGallery
from biolearn.data_library import GeoData

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set project root directory
BACKEND_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BACKEND_ROOT / 'data' / 'biolearn_output'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# not used
def read_model_probes(file_path: Union[str, Path]) -> pd.Series:
    """
    Read the model probes from a CSV file.
    
    :param file_path: Path to the CSV file containing model probes
    :return: Series of model probes
    """
    model_probes = pd.read_csv(file_path, header=None, names=['probeID'])
    return model_probes['probeID']

# not used
def get_unique_methylation_sites(models: List[str]) -> np.ndarray:
    """
    Get unique methylation sites for given models.
    
    :param models: List of model names
    :return: Array of unique methylation sites
    """
    gallery = ModelGallery()
    all_sites = []

    for model in models:
        sites = gallery.get(model).methylation_sites()
        logger.info(f'Model {model} has {len(sites)} sites')
        all_sites.extend(sites)

    unique_sites = np.unique(all_sites)
    return unique_sites

def process_biolearn_models(data: GeoData, models: List[str]) -> pd.DataFrame:
    """
    Process biolearn models and return combined results.
    
    :param data: GeoData object containing methylation data
    :param models: List of model names to process
    :return: Combined DataFrame of all model results
    """
    gallery = ModelGallery()
    results = []

    for i, model in enumerate(models, 1):
        logger.info(f"Processing model {i}: {model}")
        try:
            df = gallery.get(model).predict(data)
            df = df.add_prefix(f"{model}_")
            results.append(df)
        except Exception as e:
            logger.error(f"Error processing model {model}: {str(e)}")

    combined_df = pd.concat(results, axis=1)
    return combined_df

def save_model_results(results: pd.DataFrame, output_file: str) -> str:
    """
    Save the combined model results to a CSV file.
    
    :param results: Combined DataFrame of all model results
    :param output_file: Name of the output file
    """
    output_path = OUTPUT_DIR / output_file
    results.to_csv(output_path, index=True)
    logger.info(f"Results saved to {output_path}")
    return output_path.relative_to(BACKEND_ROOT).as_posix()

def run_biolearn(methylation_data: pd.DataFrame, metadata: Dict[str, List], models: List[str], output_file: str):
    """
    Run the complete biolearn analysis pipeline.
    
    :param methylation_data: DataFrame containing methylation data
    :param metadata: Dictionary containing metadata (age, sex)
    :param models: List of model names to process
    :param output_file: Name of the output file
    """
    logger.info("Starting biolearn analysis")
    
    # Create GeoData object(a class from biolearn)
    geo_data = GeoData.from_methylation_matrix(methylation_data)
    geo_data.metadata['age'] = metadata['age']
    geo_data.metadata['sex'] = metadata['sex'] # 1是女性，2是男性
    
    # Process models
    results_df = process_biolearn_models(geo_data, models)
    # results = [ModelGallery().get(model).predict(geo_data) for model in models]
    
    # Save results
    relative_path = save_model_results(results_df, output_file)
    logger.info(f"Processed data saved. Relative path: {relative_path}")
    
    logger.info("Biolearn analysis completed")
    return results_df

if __name__ == "__main__":
    # Example usage
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from app.services.sa2bl_processor import sa2bl_from_csv
    
    # methylation_data = sa2bl_from_csv("our_all_samples_normed_processed.csv", "our_all_samples_cell_proportions.csv")
    beta_table_path = BACKEND_ROOT / 'data' / 'processed_beta_table' / 'our_all_samples_normed_processed.csv'
    methylation_data = pd.read_csv(beta_table_path, index_col='probeID')
    metadata = {
        'age': [42, 42, 43, 43, 43, 28, 28, 28, 42, 42, 43, 43, 43, 28, 28, 28],
        'sex': [2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1]
    }
    models = ["Horvathv2","DunedinPACE"]
    # models = ["Horvathv2"]

    
    result = run_biolearn(methylation_data, metadata, models, "biolearn_results.csv")
    logger.info(f'biolearn result: {result}')
