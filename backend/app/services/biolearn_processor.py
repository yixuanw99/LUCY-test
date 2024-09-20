# app/services/biolearn_processor.py
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import List, Dict, Union
from biolearn.model_gallery import ModelGallery
from biolearn.data_library import GeoData
import io
from app.services.gcs_storage import GCSStorage

class BioLearnProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.gallery = ModelGallery()
        self.gcs_storage = GCSStorage()

    def process_biolearn_models(self, data: GeoData, models: List[str]) -> pd.DataFrame:
        """
        Process biolearn models and return combined results.
        
        :param data: GeoData object containing methylation data
        :param models: List of model names to process
        :return: Combined DataFrame of all model results
        """
        results = []
        for i, model in enumerate(models, 1):
            self.logger.info(f"Processing model {i}: {model}")
            try:
                df = self.gallery.get(model).predict(data)
                df = df.add_prefix(f"{model}_")
                results.append(df)
            except Exception as e:
                self.logger.error(f"Error processing model {model}: {str(e)}")
        return pd.concat(results, axis=1)

    def save_model_results(self, results: pd.DataFrame, output_file: str) -> str:
        """
        Save the combined model results to a CSV file in GCS.
        
        :param results: Combined DataFrame of all model results
        :param output_file: Name of the output file
        :return: GCS URL of the saved file
        """
        gcs_path = f"data/biolearn_output/{output_file}"
        csv_buffer = io.StringIO()
        results.to_csv(csv_buffer, index=True)
        csv_string = csv_buffer.getvalue()
        
        gcs_url = self.gcs_storage.upload_string(csv_string, gcs_path)
        self.logger.info(f"Results saved to GCS: {gcs_url}")
        return gcs_url

    def run_biolearn(self, methylation_data: pd.DataFrame, metadata: Dict[str, List], models: List[str], output_file: str):
        """
        Run the complete biolearn analysis pipeline.
        
        :param methylation_data: DataFrame containing methylation data
        :param metadata: Dictionary containing metadata (age, sex)
        :param models: List of model names to process
        :param output_file: Name of the output file
        """
        self.logger.info("Starting biolearn analysis")
        geo_data = GeoData.from_methylation_matrix(methylation_data)
        geo_data.metadata['age'] = metadata['age']
        geo_data.metadata['sex'] = metadata['sex']
        results_df = self.process_biolearn_models(geo_data, models)
        relative_path = self.save_model_results(results_df, output_file)
        self.logger.info(f"Processed data saved. Relative path: {relative_path}")
        self.logger.info("Biolearn analysis completed")
        return results_df

    # 有點問題，還沒使用，應該不會用到，因為前一步會傳來pd.DataFrame
    def run_biolearn_with_gcs(self, methylation_data_gcs_path: str, metadata: Dict[str, List], models: List[str]):
        """
        Run the complete biolearn analysis pipeline.
        
        :param methylation_data_gcs_path: GCS path to the CSV file containing methylation data
        :param metadata: Dictionary containing metadata (age, sex)
        :param models: List of model names to process
        :return: Results DataFrame and GCS URL of the saved file
        """
        self.logger.info("Starting biolearn analysis")
        
        # Download methylation data from GCS
        methylation_csv = self.gcs_storage.download_as_text_utf8(methylation_data_gcs_path)
        methylation_data = pd.read_csv(io.StringIO(methylation_csv), index_col='probeID')
        
        geo_data = GeoData.from_methylation_matrix(methylation_data)
        geo_data.metadata['age'] = metadata['age']
        geo_data.metadata['sex'] = metadata['sex']
        results_df = self.process_biolearn_models(geo_data, models)
        self.logger.info("Biolearn analysis completed")
        return results_df


if __name__ == "__main__":
    from pathlib import Path
    import pandas as pd
   
    processor = BioLearnProcessor()
    
    # 示例用法
    # beta_table_path = processor.backend_root / 'data' / 'processed_beta_table' / 'our_all_samples_processed.csv'
    # methylation_data = pd.read_csv(beta_table_path, index_col='probeID')
    # metadata = {
    #     'age': [42, 42, 43, 43, 43, 28, 28, 28, 42, 42, 43, 43, 43, 28, 28, 28],
    #     'sex': [2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1]
    # }
    # models = ["Horvathv2", "DunedinPACE"]
    
    # result = processor.run_biolearn(methylation_data, metadata, models, "biolearn_results.csv")
    # processor.logger.info(f'BioLearn result: {result}')

    # 示例用法 for run_biolearn_with_gcs
    methylation_data_gcs_path = "data/processed_beta_table/our_all_samples_processed.csv"
    metadata = {
        'age': [42, 42, 43, 43, 43, 28, 28, 28, 42, 42, 43, 43, 43, 28, 28, 28],
        'sex': [2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1]
    }
    models = ["Horvathv2", "DunedinPACE"]
    
    result, gcs_url = processor.run_biolearn(methylation_data_gcs_path, metadata, models, "biolearn_results.csv")
    processor.logger.info(f'BioLearn result: {result}')
    processor.logger.info(f'Results saved to GCS: {gcs_url}')