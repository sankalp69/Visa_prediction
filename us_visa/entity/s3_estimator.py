from us_visa.cloud_storage.aws_storage import SimpleStorageService
from us_visa.exception import USvisaException
from us_visa.entity.estimator import USvisaModel
import sys
from pandas import DataFrame


class GCSEstimator:
    """
    This class is responsible for storing and retrieving model artifacts from Google Cloud Storage
    """
    
    def __init__(self, bucket_name: str, model_path: str):
        self.bucket_name = bucket_name
        self.model_path = model_path
        self.storage = SimpleStorageService()
        
    def save_model(self, model, model_name: str):
        """
        Save model to Google Cloud Storage
        """
        try:
            model_file_path = f"{self.model_path}/{model_name}"
            self.storage.upload_file(model, model_file_path)
            return True
        except Exception as e:
            raise e
    
    def load_model(self, model_name: str):
        """
        Load model from Google Cloud Storage
        """
        try:
            model_file_path = f"{self.model_path}/{model_name}"
            local_path = f"/tmp/{model_name}"
            self.storage.download_file(model_file_path, local_path)
            return local_path
        except Exception as e:
            raise e