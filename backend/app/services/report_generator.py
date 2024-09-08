# app/services/report_generator.py
from .idat_processor import process_idat_file
from datetime import date

def generate_report(idat_file):
    processed_data = process_idat_file(idat_file)
    
    return {
        "name": "測試用戶",  # This should be fetched from user data in a real scenario
        "collection_date": date.today(),
        "report_date": date.today(),
        "bio_age": processed_data["bio_age"],
        "chro_age": processed_data["chro_age"],
        "pace_value": processed_data["pace_value"],
        "pace_pr": processed_data["pace_pr"],
        # ... other fields ...
    }