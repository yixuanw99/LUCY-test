# app/services/report_generator.py
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from scipy import stats
from typing import Dict, Union, List
import random
import logging
from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from app.services.idat_processor import IDATProcessor
from app.services.r_epidish_processor import EpiDISHProcessor
from app.services.sa2bl_processor import SA2BLProcessor
from app.services.biolearn_processor import BioLearnProcessor
from app.services.r_epigentl_processor import EpigenTLProcessor
from app.services.mentalhealth_processor import MentalHealthProcessor
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

def cap_pr(value):
    """
    將PR值限制在0到100之間。
    """
    return max(0, min(100, value))

class ReportGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.processed_data = None
        self.processed_data_path = None
        self.epidish_data = None
        self.sa2bl_data = None
        self.biolearn_result_Horvathv2 = None
        self.biolearn_result_DunedinPACE = None
        self.epigentl_result = None
        self.mentalhealth_result = None
        self.population_data = None
        self.epidish_processor = EpiDISHProcessor()
        self.sa2bl_processor = SA2BLProcessor()
        self.biolearn_processor = BioLearnProcessor()
        self.epigentl_processor = EpigenTLProcessor()
        self.mentalhealth_processor = MentalHealthProcessor(classifier='logistic')

    def _run_epidish(self):
        self.epidish_data = self.epidish_processor.run_epidish_with_csv(self.processed_data_path)

    def _perform_sa2bl(self):
        self.sa2bl_data = self.sa2bl_processor.sa2bl_from_pd(self.processed_data, self.epidish_data)

    def _run_biolearn(self, metadata=None):
        self.biolearn_result_Horvathv2 = self.biolearn_processor.run_biolearn(
            self.processed_data, ["Horvathv2"], "temp_biolearn_results.csv", metadata=metadata)
        self.biolearn_result_DunedinPACE = self.biolearn_processor.run_biolearn(
            self.sa2bl_data, ["DunedinPACE"], "temp_biolearn_results.csv", metadata=metadata)
        
    def _run_epigentl(self):
        self.epigentl_result = self.epigentl_processor.run_epigentl_with_csv(self.processed_data_path)

    def _run_mentalhealth(self):
        mentalhealth_features = ['DNAmADM_C_Pred', 'DNAmCystatinC_C_Pred', 'DNAmPAI1_C_Pred', 'DNAmTIMP1_C_Pred']
        mentalhealth_data = pd.DataFrame({
            feature: [getattr(self.epigentl_result, feature).iloc[i] for i in range(len(self.processed_data.columns))]
            for feature in mentalhealth_features
        }, index=self.processed_data.columns)
        
        self.mentalhealth_result = self.mentalhealth_processor.predict_mentalhealth(mentalhealth_data)

    def load_population_data(self, csv_path=None, metadata=None):
        try:
            if csv_path and metadata:
                # 從 CSV 文件加載數據
                df = pd.read_csv(csv_path)
                
                # 確保 metadata 包含必要的信息
                if 'age' in metadata and 'sex' in metadata:
                    # 假設 metadata 只包含一個樣本的信息
                    age = metadata['age'][0]
                    sex = metadata['sex'][0]

                    self.logger.info(f"Processing data for age: {age}, sex: {sex}")
                    
                    # 定義年齡組
                    if age < 40:
                        age_group = (df['age'] < 40)
                    elif 40 <= age < 60:
                        age_group = (df['age'] >= 40) & (df['age'] < 60)
                    else:
                        age_group = (df['age'] >= 60)
                    
                    # 將 metadata 中的 'sex' 值轉換為與 CSV 中 'gender' 列匹配的格式
                    if sex == False:
                        gender = "Female"
                    elif sex == True:
                        gender = "Male"
                    else:
                        gender = None

                    # 篩選同年齡層和同性別的數據
                    if gender is not None:
                        self.population_data = df[age_group & (df['gender'] == gender)]
                    elif age is not None and not np.isnan(age):
                        self.population_data = df[age_group]
                        self.logger.warning(f"no gender information provided in metadata. Using data for age group {age_group}")
                    else:
                        self.logger.warning("Metadata does not contain age or sex information. Using all data.")
                        self.population_data = df
                    self.logger.info(f"Filtered data: {len(self.population_data)} rows")
                else:
                    self.logger.warning("Metadata does not contain age and sex information. Setting population_data to None.")
                    self.population_data = None
            else:
                self.logger.info("No CSV path or metadata provided. Setting population_data to None.")
                self.population_data = None
            
            # # 硬編碼的數據（已註釋）
            # self.population_data = pd.DataFrame({
            #     'fitage': [29.219, 50.46631, 61.1163, 67.76352, 72.28644, 75.15615, 77.44028, 80.22087, 82.6989, 86.1581, 100.1406],
            #     'vo2max': [30.0562, 36.1469, 36.75708, 37.14681, 37.48146, 37.8964, 38.25902, 38.62972, 39.22418, 39.97038, 43.359],
            #     'grip': [26.9162, 30.48044, 31.49458, 32.38475, 33.1172, 33.81915, 34.38916, 35.1858, 36.54686, 38.88269, 48.9712],
            #     'gait': [1.2357, 1.51273, 1.57494, 1.61249, 1.64798, 1.6794, 1.71936, 1.7815, 1.8631, 1.974, 2.3878],
            #     'mentalhealth': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            # })
            
            self.logger.info("Population data loaded successfully.")
        except Exception as e:
            self.logger.error(f"Error loading population data: {str(e)}", exc_info=True)
            self.population_data = None
                    
    def generate_report(self, metadata=None, mentalhealth_classifier='logistic') -> List[Dict[str, Dict[str, Union[str, float, datetime]]]]:
        # If the classifier has changed, reinitialize the MentalHealthProcessor
        if mentalhealth_classifier != self.mentalhealth_processor.classifier:
            self.mentalhealth_processor = MentalHealthProcessor(classifier=mentalhealth_classifier)
        
        self._run_epidish()
        self._perform_sa2bl()
        self._run_biolearn(metadata)
        self._run_epigentl()
        self._run_mentalhealth()

        # 確保已加載母體數據 (位置目前先寫死)
        GSEs_path = BACKEND_ROOT / 'app' / 'resources' / 'population_salivas' / 'GSEs.csv'
        # "../resources/population_salivas/GSEs.csv"

        reports = []
        for i, sample_name in enumerate(self.processed_data.columns):
            self.logger.info(f"Generating report for sample {sample_name}")
            self.logger.info(f"sample gender: {metadata['sex'][i]}")
            self.logger.info(f"sample age: {float(metadata['age'][i])}")

            # 为每个样本加载特定的人群数据
            sample_metadata = {
                'age': [metadata['age'][i]],
                'sex': [metadata['sex'][i]]
            }
            self.load_population_data(GSEs_path, metadata=sample_metadata)
            bio_age = self.biolearn_result_Horvathv2['Horvathv2_Predicted'].iloc[i]
            pace_value = self.biolearn_result_DunedinPACE['DunedinPACE_Predicted'].iloc[i] - 0.059355713  # 582人跑出來的sa2bl平均值，直接平移來跟dunedinPACE對齊(都用1.0當人羣mean)
            fitage = self.epigentl_result['DNAmFitAge_C_Pred'].iloc[i]
            vo2max = self.epigentl_result['DNAmVO2max_C_Pred'].iloc[i]
            grip = self.epigentl_result['DNAmGrip_noAge_C_Pred'].iloc[i]
            gait = self.epigentl_result['DNAmGait_noAge_C_Pred'].iloc[i]
            mentalhealth = self.mentalhealth_result['probabilities'][i]
            cystatin = self.epigentl_result['DNAmCystatinC_C_Pred'].iloc[i]
            adm = self.epigentl_result['DNAmADM_C_Pred'].iloc[i]
            timp = self.epigentl_result['DNAmTIMP1_C_Pred'].iloc[i]
            pai1 = self.epigentl_result['DNAmPAI1_C_Pred'].iloc[i]
            packyrs = self.epigentl_result['DNAmPACKYRS_C_Pred'].iloc[i]

            # 計算百分位數
            pace_pr = stats.norm.cdf(pace_value, loc=1, scale=0.2) * 100
            if self.population_data is not None:
                fitage_pr = cap_pr((self.population_data['fitage'] < fitage).mean() * 100) if 'fitage' in self.population_data.columns else None
                vo2max_pr = cap_pr((self.population_data['vo2max'] < vo2max).mean() * 100) if 'vo2max' in self.population_data.columns else None
                grip_pr = cap_pr((self.population_data['grip'] < grip).mean() * 100) if 'grip' in self.population_data.columns else None
                gait_pr = cap_pr((self.population_data['gait'] < gait).mean() * 100) if 'gait' in self.population_data.columns else None
                mentalhealth_pr = cap_pr((self.population_data['mentalhealth'] < mentalhealth).mean() * 100) if 'mentalhealth' in self.population_data.columns else None
            else:
                self.logger.warning("Population data not available. Percentile ranks will be set to None.")
                vo2max_pr = grip_pr = gait_pr = fitage_pr = mentalhealth_pr = None
            
            report = {
                sample_name: {
                    "sample_name": sample_name,
                    "gender": metadata['sex'][i],
                    "age": float(metadata['age'][i]),
                    "cdt": datetime.now(timezone.utc),
                    "bio_age": bio_age,
                    "pace_value": pace_value,
                    "pace_pr": pace_pr,
                    "fitage": fitage,
                    "fitage_pr": fitage_pr,
                    "vo2max": vo2max,
                    "vo2max_pr": vo2max_pr,
                    "grip": grip,
                    "grip_pr": grip_pr,
                    "gait": gait,
                    "gait_pr": gait_pr,
                    "mentalhealth": mentalhealth,
                    "mentalhealth_pr": mentalhealth_pr,
                    "cystatin": cystatin,
                    "adm": adm,
                    "timp": timp,
                    "pai1": pai1,
                    "packyrs": packyrs
                }
            }
            reports.append(report)

        return reports

    def save_reports(self, reports: List[Dict[str, Dict[str, Union[str, float, datetime]]]]) -> List[Report]:
        db = SessionLocal()
        try:
            saved_reports = []
            for report_data in reports:
                for sample_name, data in report_data.items():
                    # 查找對應的 SampleData
                    sample = db.query(SampleData).filter(SampleData.sample_name == sample_name).first()
                    if not sample:
                        self.logger.warning(f"Sample with name {sample_name} not found in database.")
                        continue

                    new_report = Report(
                        order_ecid=data['sample_name'],
                        gender=data['gender'],
                        age=data['age'],
                        cdt=data['cdt'],
                        bio_age=data['bio_age'],
                        pace_value=data['pace_value'],
                        pace_pr=data['pace_pr'],
                        fitage=data['fitage'],
                        fitage_pr=data['fitage_pr'],
                        vo2max=data['vo2max'],
                        vo2max_pr=data['vo2max_pr'],
                        grip=data['grip'],
                        grip_pr=data['grip_pr'],
                        gait=data['gait'],
                        gait_pr=data['gait_pr'],
                        mentalhealth=data['mentalhealth'],
                        mentalhealth_pr=data['mentalhealth_pr'],
                        cystatin=data['cystatin'],
                        adm=data['adm'],
                        timp=data['timp'],
                        pai1=data['pai1'],
                        packyrs=data['packyrs']
                    )
                    db.add(new_report)
                    saved_reports.append(new_report)
            db.commit()
            return saved_reports
        finally:
            db.close()

    def generate_and_save_reports(self, metadata=None, mentalhealth_classifier='logistic') -> List[Report]:
        reports = self.generate_report(metadata=metadata, mentalhealth_classifier=mentalhealth_classifier)
        return self.save_reports(reports)

class IdatReportGenerator(ReportGenerator):
    def __init__(self):
        super().__init__()
        self.idat_processor = IDATProcessor()

    def process_data(self, pd_file_path: str, idat_file_path: str, batch_name: str = "report_test01"):
        raw_data = self.idat_processor.process_idat(pd_file_path, idat_file_path)
        self.processed_data = self.idat_processor.champ_df_postprocess(raw_data)
        self.processed_data_path = self.idat_processor.save_processed_data(self.processed_data, batch_name=batch_name)

class ProcessedDataReportGenerator(ReportGenerator):
    def process_data(self, processed_data_path: str):
        self.processed_data_path = processed_data_path
        self.processed_data = pd.read_csv(self.processed_data_path, index_col='probeID')

    def _perform_sa2bl(self):
        self.sa2bl_data = self.sa2bl_processor.sa2bl(self.processed_data_path, self.epidish_data)

    def _run_biolearn(self, metadata=None):
        self.biolearn_result_Horvathv2 = self.biolearn_processor.run_biolearn(
            self.processed_data_path, ["Horvathv2"], "temp_biolearn_results.csv", metadata=metadata)
        self.biolearn_result_DunedinPACE = self.biolearn_processor.run_biolearn(
            self.sa2bl_data, ["DunedinPACE"], "temp_biolearn_results.csv", metadata=metadata)

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
