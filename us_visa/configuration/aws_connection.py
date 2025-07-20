import os
from google.cloud import storage
from us_visa.constants import GCP_PROJECT_ID_ENV_KEY, GCP_REGION

class GCSClient:
    """
    This Class gets Google Cloud credentials from env_variable and creates a connection with GCS bucket
    """
    
    def __init__(self):
        self.__project_id = os.getenv(GCP_PROJECT_ID_ENV_KEY, )
        self.__region = GCP_REGION
        
        if not self.__project_id:
            raise Exception(f"Environment variable: {GCP_PROJECT_ID_ENV_KEY} is not set.")
        
        # Initialize Google Cloud Storage client
        self.client = storage.Client(project=self.__project_id)
        
    def get_gcs_client(self):
        """
        Returns Google Cloud Storage client
        """
        return self.client
    
    def get_project_id(self):
        """
        Returns GCP project ID
        """
        return self.__project_id
        