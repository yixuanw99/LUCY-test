# app/services/biolearn_processor.py
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import List, Dict, Union
from biolearn.model_gallery import ModelGallery
from biolearn.data_library import GeoData

class BioLearnProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.backend_root = Path(__file__).resolve().parents[2]
        self.output_dir = self.backend_root / 'data' / 'biolearn_output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.gallery = ModelGallery()

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
        Save the combined model results to a CSV file.
        
        :param results: Combined DataFrame of all model results
        :param output_file: Name of the output file
        """
        output_path = self.output_dir / output_file
        results.to_csv(output_path, index=True)
        self.logger.info(f"Results saved to {output_path}")
        return output_path.relative_to(self.backend_root).as_posix()

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


if __name__ == "__main__":
    from pathlib import Path
    import pandas as pd
   
    processor = BioLearnProcessor()
    
    # 示例用法
    beta_table_path = processor.backend_root / 'data' / 'processed_beta_table' / 'our_all_samples_normed_processed.csv'
    methylation_data = pd.read_csv(beta_table_path, index_col='probeID')
    metadata = {
        'age': [42, 42, 43, 43, 43, 28, 28, 28, 42, 42, 43, 43, 43, 28, 28, 28],
        'sex': [2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1]
    }
    models = ["Horvathv2", "DunedinPACE"]
    
    result = processor.run_biolearn(methylation_data, metadata, models, "biolearn_results.csv")
    processor.logger.info(f'BioLearn result: {result}')