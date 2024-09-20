# backend/scripts_manual/upload_idat.py
import os
from google.cloud import storage
from google.oauth2 import service_account
from dotenv import load_dotenv
import argparse

# 加載 .env.development 文件
load_dotenv('.env.development')

def get_storage_client():
    # 使用環境變量中指定的服務賬號密鑰文件
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    )
    return storage.Client(credentials=credentials)

def upload_file_to_gcs(bucket_name, source_file, destination_blob_name):
    """上傳單個文件到 GCS"""
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file)
    print(f"File {source_file} uploaded to {destination_blob_name}.")

def upload_directory_to_gcs(bucket_name, source_dir, destination_prefix):
    """上傳整個目錄到 GCS"""
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)

    for root, _, files in os.walk(source_dir):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, source_dir)
            gcs_path = os.path.join(destination_prefix, relative_path)

            blob = bucket.blob(gcs_path)
            blob.upload_from_filename(local_path)
            print(f"File {local_path} uploaded to {gcs_path}.")

def main():
    # example: python scripts_manual/upload_idat.py data/raw/run1 data/raw/run1/
    parser = argparse.ArgumentParser(description="Upload files or directories to Google Cloud Storage")
    parser.add_argument("source", help="Source file or directory to upload")
    parser.add_argument("destination", help="Destination path in GCS")
    parser.add_argument("--bucket", help="GCS bucket name (overrides env variable)")
    args = parser.parse_args()

    bucket_name = args.bucket or os.getenv('GCS_BUCKET_NAME')
    if not bucket_name:
        raise ValueError("GCS bucket name not provided and not found in environment variables")

    if os.path.isfile(args.source):
        upload_file_to_gcs(bucket_name, args.source, args.destination)
    elif os.path.isdir(args.source):
        upload_directory_to_gcs(bucket_name, args.source, args.destination)
    else:
        print(f"Error: {args.source} is neither a file nor a directory")

if __name__ == "__main__":
    main()