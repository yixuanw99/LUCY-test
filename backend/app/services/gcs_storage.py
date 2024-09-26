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

    def upload_string(self, string_data: str, destination_blob_name: str):
        """Uploads a string to the bucket."""
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_string(string_data)
        return f"gs://{self.bucket_name}/{destination_blob_name}"
    
    def download_as_text_utf8(self, gcs_path: str) -> str:
        """
        Download a file from Google Cloud Storage and return its content as a string.

        :param gcs_path: The path to the file in GCS
        :return: The content of the file as a string
        """
        try:
            # 從 GCS 路徑中提取對象名稱
            if gcs_path.startswith(f"gs://{self.bucket_name}/"):
                object_name = gcs_path[len(f"gs://{self.bucket_name}/"):]
            else:
                object_name = gcs_path

            blob = self.bucket.blob(object_name)
            
            # 下載為字節並解碼為字符串
            content = blob.download_as_text(encoding="utf-8")
            
            return content
        except Exception as e:
            raise Exception(f"Error downloading file from GCS: {str(e)}")
        
    def list_blobs(self, prefix: str):
        """
        List all blobs in the bucket with the given prefix.
        
        :param prefix: The prefix to filter blobs
        :return: An iterable of blob objects
        """
        return self.bucket.list_blobs(prefix=prefix)