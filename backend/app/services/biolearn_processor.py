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

def read_model_probes(file_path: Union[str, Path]) -> pd.Series:
    """
    Read the model probes from a CSV file.
    
    :param file_path: Path to the CSV file containing model probes
    :return: Series of model probes
    """
    model_probes = pd.read_csv(file_path, header=None, names=['probeID'])
    return model_probes['probeID']

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

def save_model_results(results: pd.DataFrame, output_file: str):
    """
    Save the combined model results to a CSV file.
    
    :param results: Combined DataFrame of all model results
    :param output_file: Name of the output file
    """
    output_path = OUTPUT_DIR / output_file
    results.to_csv(output_path, index=True)
    logger.info(f"Results saved to {output_path}")

def run_biolearn_analysis(methylation_data: pd.DataFrame, metadata: Dict[str, List], models: List[str], output_file: str):
    """
    Run the complete biolearn analysis pipeline.
    
    :param methylation_data: DataFrame containing methylation data
    :param metadata: Dictionary containing metadata (age, sex)
    :param models: List of model names to process
    :param output_file: Name of the output file
    """
    logger.info("Starting biolearn analysis")
    
    # Create GeoData object
    geo_data = GeoData.from_methylation_matrix(methylation_data)
    geo_data.metadata['age'] = metadata['age']
    geo_data.metadata['sex'] = metadata['sex']
    geo_data.metadata.set_index('probeID', inplace=True)
    
    # Process models
    results = process_biolearn_models(geo_data, models)
    
    # Save results
    save_model_results(results, output_file)
    
    logger.info("Biolearn analysis completed")

if __name__ == "__main__":
    # Example usage
    from app.services.sa2bl_processor import sa2bl_from_csv
    
    methylation_data = sa2bl_from_csv("our_all_samples_normed_processed.csv", "our_all_samples_cell_proportions.csv")
    metadata = {
        'age': [50, 64, 57, 65, 56, 56, 57, 51, 53, 70, 61, 60, 66, 72, 61, 56],
        'sex': [1] * 16
    }
    models = ["Horvathv1", "Hannum", "PhenoAge", "GrimAgeV2", "DunedinPACE"]
    
    run_biolearn_analysis(methylation_data, metadata, models, "biolearn_results.csv")