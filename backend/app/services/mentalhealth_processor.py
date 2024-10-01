# app/services/mentalhealth_processor.py
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
import logging
from typing import Dict, Union, List

class MentalHealthProcessor:
    def __init__(self, classifier='logistic'):
        self.logger = logging.getLogger(__name__)
        self.backend_root = Path(__file__).resolve().parents[2]
        self.resource_dir = self.backend_root / 'app' / 'resources'
        self.classifier = classifier
        self.model_file = self.resource_dir / 'mentalhealth_assets' / f'mdd_prediction_{classifier}.pkl'
        self.blood_data_file = self.resource_dir / 'mentalhealth_assets' / 'biolearn_GSE201287_training.csv'
        self.model = self.load_model()
        self.blood_data = self.load_blood_data()
        self.feature_mapping = {
            'adm': 'DNAmADM_C_Pred',
            'cystatin': 'DNAmCystatinC_C_Pred',
            'pai1': 'DNAmPAI1_C_Pred',
            'timp': 'DNAmTIMP1_C_Pred'
        }
        self.logger.info(f"MentalHealthProcessor initialized with classifier: {classifier}")

    def load_model(self):
        self.logger.info(f"Loading model from file: {self.model_file}")
        if not self.model_file.exists():
            self.logger.error(f"Model file not found: {self.model_file}")
            raise FileNotFoundError(f"Model file not found: {self.model_file}")
        model = joblib.load(self.model_file)
        self.logger.info("Model loaded successfully")
        return model

    def load_blood_data(self):
        self.logger.info(f"Loading blood data from file: {self.blood_data_file}")
        if not self.blood_data_file.exists():
            self.logger.error(f"Blood data file not found: {self.blood_data_file}")
            raise FileNotFoundError(f"Blood data file not found: {self.blood_data_file}")
        blood_data = pd.read_csv(self.blood_data_file)
        self.logger.info("Blood data loaded successfully")
        return blood_data

    def quantile_transform(self, saliva_df: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("Performing quantile transformation")
        transformed_saliva = pd.DataFrame()
        for training_feature, db_feature in self.feature_mapping.items():
            self.logger.info(f"Transforming feature: {db_feature} to {training_feature}")
            blood_quantiles = np.percentile(self.blood_data[training_feature], np.arange(0, 101))
            saliva_quantiles = np.percentile(saliva_df[db_feature], np.arange(0, 101))
            transformed_saliva[training_feature] = np.interp(saliva_df[db_feature], saliva_quantiles, blood_quantiles)
        self.logger.info("Quantile transformation completed")
        return transformed_saliva

    def predict_mentalhealth(self, saliva_data: pd.DataFrame) -> Dict[str, Union[np.ndarray, np.ndarray]]:
        self.logger.info("Predicting mental health")
        self.logger.info(f"Using features: {list(self.feature_mapping.values())}")
        X_transformed = self.quantile_transform(saliva_data)
        
        self.logger.info("Making predictions")
        predictions = self.model.predict(X_transformed)
        probabilities = self.model.predict_proba(X_transformed)[:, 1]
        
        self.logger.info("Predictions completed")
        return {
            'predictions': predictions,
            'probabilities': probabilities
        }