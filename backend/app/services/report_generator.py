# app/services/report_generator.py
import pandas as pd
import numpy as np
from datetime import date
from scipy import stats
from typing import Dict, Union, List
from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
import logging
from app.services.idat_processor import IDATProcessor
from app.services.r_epidish_processor import EpiDISHProcessor
from app.services.sa2bl_processor import SA2BLProcessor
from app.services.biolearn_processor import BioLearnProcessor
# from app.services.r_epigentl_processor import EpigentlProcessor
from app.db.models import Report, SampleData
from app.db.session import SessionLocal

# Set project root directory
BACKEND_ROOT = Path(__file__).resolve().parents[2]

def setup_logging():
    log_dir = BACKEND_ROOT / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'application.log'

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


class ReportGenerator:
    def __init__(self):
        self.processed_data = None
        self.processed_data_path = None
        self.epidish_data = None
        self.sa2bl_data = None
        self.biolearn_result_Horvathv2 = None
        self.biolearn_result_DunedinPACE = None
        self.epidish_processor = EpiDISHProcessor()
        self.sa2bl_processor = SA2BLProcessor()
        self.biolearn_processor = BioLearnProcessor()

    def _run_epidish(self):
        self.epidish_data = self.epidish_processor.run_epidish_with_csv(self.processed_data_path)

    def _perform_sa2bl(self):
        self.sa2bl_data = self.sa2bl_processor.sa2bl_from_pd(self.processed_data, self.epidish_data)

    def _run_biolearn(self, metadata=None):
        self.biolearn_result_Horvathv2 = self.biolearn_processor.run_biolearn(
            self.processed_data, ["Horvathv2"], "temp_biolearn_results.csv", metadata=metadata)
        self.biolearn_result_DunedinPACE = self.biolearn_processor.run_biolearn(
            self.sa2bl_data, ["DunedinPACE"], "temp_biolearn_results.csv", metadata=metadata)

    def generate_report(self, metadata=None) -> List[Dict[str, Dict[str, Union[str, float, date]]]]:
        self._run_epidish()
        self._perform_sa2bl()
        self._run_biolearn(metadata)

        reports = []
        for i, sample_name in enumerate(self.processed_data.columns):
            bio_age = self.biolearn_result_Horvathv2['Horvathv2_Predicted'].iloc[i]
            chro_age = metadata['age'][i] if metadata and 'age' in metadata else 0
            pace_value = self.biolearn_result_DunedinPACE['DunedinPACE_Predicted'].iloc[i]
            pace_pr = stats.norm.cdf(pace_value, loc=1, scale=0.2) * 100

            report = {
                sample_name: {
                    "sample_name": sample_name,
                    "collection_date": date(2023, 1, 1),  # Placeholder date
                    "report_date": date.today(),
                    "bio_age": bio_age,
                    "chro_age": chro_age,
                    "pace_value": pace_value,
                    "pace_pr": pace_pr
                }
            }
            reports.append(report)

        return reports

    def save_reports(self, reports: List[Dict[str, Dict[str, Union[str, float, date]]]]) -> List[Report]:
        db = SessionLocal()
        try:
            saved_reports = []
            for report_data in reports:
                for sample_name, data in report_data.items():
                    # 查找對應的 SampleData
                    sample = db.query(SampleData).filter(SampleData.sample_name == sample_name).first()
                    if not sample:
                        logging.warning(f"Sample with name {sample_name} not found in database.")
                        continue

                    new_report = Report(
                        order_id=sample.id,
                        collection_date=data['collection_date'],
                        report_date=data['report_date'],
                        bio_age=data['bio_age'],
                        chro_age=data['chro_age'],
                        pace_value=data['pace_value'],
                        pace_pr=data['pace_pr']
                    )
                    db.add(new_report)
                    saved_reports.append(new_report)
            db.commit()
            return saved_reports
        finally:
            db.close()

    def generate_and_save_reports(self, metadata = None) -> List[Report]:
        reports = self.generate_report(metadata = metadata)
        return self.save_reports(reports)

class IdatReportGenerator(ReportGenerator):
    def __init__(self):
        super().__init__()
        self.idat_processor = IDATProcessor()

    def process_data(self, pd_file_path: str, idat_file_path: str):
        raw_data = self.idat_processor.process_idat(pd_file_path, idat_file_path)
        self.processed_data = self.idat_processor.champ_df_postprocess(raw_data)
        self.processed_data_path = self.idat_processor.save_processed_data(self.processed_data, "report_test01")

class ProcessedDataReportGenerator(ReportGenerator):
    def process_data(self, processed_data_path: str):
        self.processed_data_path = processed_data_path
        self.processed_data = pd.read_csv(self.processed_data_path, index_col='probeID')

if __name__ == "__main__":
    # 在主程序開始時調用
    setup_logging()
    
    # Example metadata
    # TODO: Replace with user.age and user.sex
    metadata = {
        'age': [42, 42, 43, 43, 43, 28, 28, 28, 42, 42, 43, 43, 43, 28, 28, 28],
        'sex': [2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1]
    }

    # Example usage for IDAT processing
    idat_generator = IdatReportGenerator()
    idat_file_loc = BACKEND_ROOT / 'data' / 'raw' / 'run1'
    sample_sheet_path = idat_file_loc / 'Sample_Sheet.csv'
    idat_generator.process_data(sample_sheet_path, idat_file_loc)
    report_from_idat = idat_generator.generate_and_save_reports(metadata)
    print("Report from IDAT generated and saved:")

    # Example usage for processed data
    # processed_data_path = BACKEND_ROOT / 'data' / 'processed_beta_table' / 'our_all_samples_processed.csv'
    # processed_generator = ProcessedDataReportGenerator()
    # processed_generator.process_data(str(processed_data_path))
    # saved_reports = processed_generator.generate_and_save_reports(metadata)
    # print("\nReports generated and saved:")
