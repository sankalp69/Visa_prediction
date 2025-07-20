from us_visa.configuration.aws_connection import GCSClient
from us_visa.constants import GCP_BUCKET_NAME, GCP_MODEL_REGISTRY_KEY
import os
from datetime import datetime
import logging

class SimpleStorageService:
    """
    This class is responsible for storing and retrieving data from Google Cloud Storage
    """
    
    def __init__(self):
        self.gcs_client = GCSClient()
        self.bucket_name = GCP_BUCKET_NAME
        self.model_registry_key = GCP_MODEL_REGISTRY_KEY
        
    def upload_file(self, from_filename: str, to_filename: str, remove: bool = True):
        """
        Upload a file to Google Cloud Storage
        """
        try:
            logging.info(f"Uploading file from {from_filename} to {to_filename}")
            bucket = self.gcs_client.get_gcs_client().bucket(self.bucket_name)
            blob = bucket.blob(to_filename)
            blob.upload_from_filename(from_filename)
            
            if remove:
                os.remove(from_filename)
                logging.info(f"Removed local file: {from_filename}")
                
            return True
            
        except Exception as e:
            logging.error(f"Error uploading file to GCS: {e}")
            raise e
    
    def download_file(self, from_filename: str, to_filename: str):
        """
        Download a file from Google Cloud Storage
        """
        try:
            logging.info(f"Downloading file from {from_filename} to {to_filename}")
            bucket = self.gcs_client.get_gcs_client().bucket(self.bucket_name)
            blob = bucket.blob(from_filename)
            blob.download_to_filename(to_filename)
            return True
            
        except Exception as e:
            logging.error(f"Error downloading file from GCS: {e}")
            raise e
    
    def list_files(self, prefix: str = ""):
        """
        List files in Google Cloud Storage bucket
        """
        try:
            bucket = self.gcs_client.get_gcs_client().bucket(self.bucket_name)
            blobs = bucket.list_blobs(prefix=prefix)
            return [blob.name for blob in blobs]
            
        except Exception as e:
            logging.error(f"Error listing files from GCS: {e}")
            raise e
    
    def delete_file(self, filename: str):
        """
        Delete a file from Google Cloud Storage
        """
        try:
            logging.info(f"Deleting file: {filename}")
            bucket = self.gcs_client.get_gcs_client().bucket(self.bucket_name)
            blob = bucket.blob(filename)
            blob.delete()
            return True
            
        except Exception as e:
            logging.error(f"Error deleting file from GCS: {e}")
            raise e