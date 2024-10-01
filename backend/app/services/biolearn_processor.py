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
        self.processed_beta_table_dir = self.backend_root / 'data' / 'processed_beta_table'
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

    def run_biolearn(self, methylation_data: Union[str, Path, pd.DataFrame], 
                     models: List[str], output_file: str, 
                     metadata: Dict[str, List] = None):
        """
        Run the complete biolearn analysis pipeline.
        
        :param methylation_data: Either a path to the CSV file or a DataFrame containing methylation data
        :param models: List of model names to process
        :param output_file: Name of the output file
        :param metadata: Optional dictionary containing metadata (age, sex)
        """
        self.logger.info("Starting biolearn analysis")
        
        if "GrimAgeV1" in models or "GrimAgeV2" in models:
            if metadata is None or 'age' not in metadata or 'sex' not in metadata:
                raise ValueError("Metadata with 'age' and 'sex' is required for GrimAge models")
        
        # 處理 methylation_data 輸入
        if isinstance(methylation_data, (str, Path)):
            self.logger.info(f"Reading methylation data from file: {methylation_data}")
            methylation_data_path = self.processed_beta_table_dir / methylation_data
            self.logger.info(f"methylation_data_path: {methylation_data_path}")
            methylation_data = pd.read_csv(methylation_data_path, index_col='probeID')
        elif not isinstance(methylation_data, pd.DataFrame):
            raise ValueError("methylation_data must be either a file path or a pandas DataFrame")
        
        geo_data = GeoData.from_methylation_matrix(methylation_data)
        
        if metadata:
            # Get the sample names from the methylation data
            sample_names = methylation_data.columns

            # Create dictionaries to map sample names to age and sex
            age_dict = dict(zip(metadata['order_ecid'], metadata['age']))
            sex_dict = dict(zip(metadata['order_ecid'], metadata['sex']))

            # Select only the metadata for samples present in methylation_data
            selected_ages = [age_dict[sample] for sample in sample_names if sample in age_dict]
            selected_sexes = [sex_dict[sample] for sample in sample_names if sample in sex_dict]

            # Assign the selected metadata to geo_data
            geo_data.metadata['age'] = selected_ages
            geo_data.metadata['sex'] = selected_sexes

            self.logger.info(f"Metadata assigned: {len(selected_ages)} ages, {len(selected_sexes)} sexes")
        
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
    beta_table_path = processor.backend_root / 'data' / 'processed_beta_table' / 'our_all_samples_processed.csv'
    methylation_data = pd.read_csv(beta_table_path, index_col='probeID')
    metadata = {
        'age': [42, 42, 43, 43, 43, 28, 28, 28, 42, 42, 43, 43, 43, 28, 28, 28],
        'sex': [2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1]
    }
    models = ["Horvathv2", "DunedinPACE"]
    
    result = processor.run_biolearn(methylation_data, metadata, models, "biolearn_results.csv")
    processor.logger.info(f'BioLearn result: {result}')