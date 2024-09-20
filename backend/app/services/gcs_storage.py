# app/services/gcs_storage.py

from google.cloud import storage
from google.oauth2 import service_account
from app.core.config import settings
from pathlib import Path

class GCSStorage:
    def __init__(self):
        self.backend_root = Path(__file__).resolve().parents[2]
        credential_file_name = settings.GOOGLE_APPLICATION_CREDENTIALS
        credentials_path = self.backend_root / credential_file_name
        self.credentials = service_account.Credentials.from_service_account_file(
            str(credentials_path)
        )
        self.client = storage.Client(credentials=self.credentials)
        self.bucket_name = settings.GCS_BUCKET_NAME
        self.bucket = self.client.bucket(self.bucket_name)

    def upload_file(self, source_file_path: str, destination_blob_name: str):
        """Uploads a file to the bucket."""
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_path)
        return f"gs://{self.bucket_name}/{destination_blob_name}"

    def download_file(self, source_blob_name: str, destination_file_name: str):
        """Downloads a blob from the bucket."""
        blob = self.bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

    def read_csv(self, blob_name: str):
        """Reads a CSV file from GCS and returns a pandas DataFrame."""
        import pandas as pd
        import io

        blob = self.bucket.blob(blob_name)
        content = blob.download_as_text()
        return pd.read_csv(io.StringIO(content))