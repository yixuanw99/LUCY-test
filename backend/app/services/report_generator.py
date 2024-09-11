# app/services/report_generator.py
import pandas as pd
import numpy as np
import sys
from datetime import date
from scipy import stats
from typing import Dict, Union, List
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.services.idat_processor import process_idat, champ_df_postprocess, save_processed_data
from app.services.r_epidish_processor import run_epidish_with_csv
from app.services.sa2bl_processor import sa2bl_from_pd
from app.services.biolearn_processor import run_biolearn

# Set project root directory
BACKEND_ROOT = Path(__file__).resolve().parents[2]

class ReportGenerator:
    def __init__(self):
        self.processed_data = None
        self.processed_data_path = None
        self.epidish_data = None
        self.sa2bl_data = None
        self.biolearn_result_Horvathv2 = None
        self.biolearn_result_DunedinPACE = None

    def _run_epidish(self):
        self.epidish_data = run_epidish_with_csv(self.processed_data_path)

    def _perform_sa2bl(self):
        self.sa2bl_data = sa2bl_from_pd(self.processed_data, self.epidish_data)

    def _run_biolearn(self, metadata):
        self.biolearn_result_Horvathv2 = run_biolearn(self.processed_data, metadata, ["Horvathv2"], "temp_biolearn_results.csv")
        self.biolearn_result_DunedinPACE = run_biolearn(self.sa2bl_data, metadata, ["DunedinPACE"], "temp_biolearn_results.csv")

    def generate_report(self, metadata) -> List[Dict[str, Dict[str, Union[str, float, date]]]]:
        self._run_epidish()
        self._perform_sa2bl()
        self._run_biolearn(metadata)

        reports = []
        for i, sample_id in enumerate(self.processed_data.columns):
            pace_value = self.biolearn_result_DunedinPACE['DunedinPACE_Predicted'].iloc[i]
            pace_pr = stats.norm.cdf(pace_value, loc=1, scale=0.2) * 100

            report = {
                sample_id: {
                    "name": sample_id,
                    "collection_date": date(2023, 1, 1),  # Placeholder date, you might want to get this from metadata
                    "report_date": date.today(),
                    "bio_age": self.biolearn_result_Horvathv2['Horvathv2_Predicted'].iloc[i],
                    "chro_age": metadata['age'][i],
                    "pace_value": pace_value,
                    "pace_pr": pace_pr
                }
            }
            reports.append(report)

        return reports

class IdatReportGenerator(ReportGenerator):
    def process_data(self, pd_file_path: str, idat_file_path: str):
        raw_data = process_idat(pd_file_path, idat_file_path)
        self.processed_data = champ_df_postprocess(raw_data)
        self.processed_data_path = save_processed_data(self.processed_data, "report_test01")

class ProcessedDataReportGenerator(ReportGenerator):
    def process_data(self, processed_data_path: str):
        self.processed_data_path = processed_data_path
        self.processed_data = pd.read_csv(self.processed_data_path, index_col='probeID')

if __name__ == "__main__":
    # Example metadata
    metadata = {
        'age': [42, 42, 43, 43, 43, 28, 28, 28, 42, 42, 43, 43, 43, 28, 28, 28],
        'sex': [2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1]
    }

    # Example usage for IDAT processing
    # idat_generator = IdatReportGenerator()
    # idat_generator.process_data("path/to/Sample_Sheet.csv", "path/to/idat_directory")
    # report_from_idat = idat_generator.generate_report(metadata)
    # print("Report from IDAT:")
    # print(report_from_idat)

    # Example usage for processed data
    processed_data_path = BACKEND_ROOT / 'data' / 'processed_beta_table' / 'our_all_samples_normed_processed.csv'
    processed_generator = ProcessedDataReportGenerator()
    processed_generator.process_data(str(processed_data_path))
    report_from_processed = processed_generator.generate_report(metadata)
    print("\nReport from processed data:")
    print(report_from_processed)