import os, sys
from us_visa.cloud_storage.aws_storage import SimpleStorageService
from us_visa.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from us_visa.entity.config_entity import ModelPusherConfig
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.constants import MODEL_PUSHER_GCS_KEY

class ModelPusher:
    """
    This class is responsible for pushing the trained model to Google Cloud Storage
    """
    
    def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact,
                 model_pusher_config: ModelPusherConfig):
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.storage = SimpleStorageService()
        
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        This method is responsible for pushing the model to Google Cloud Storage
        """
        try:
            logging.info("Entered initiate_model_pusher method of ModelPusher class")
            
            # Push model to GCS
            self.storage.upload_file(
                from_filename=self.model_evaluation_artifact.export_model_path,
                to_filename=f"{MODEL_PUSHER_GCS_KEY}/model.pkl"
            )
            
            # Push preprocessing object to GCS
            self.storage.upload_file(
                from_filename=self.model_evaluation_artifact.export_preprocessor_path,
                to_filename=f"{MODEL_PUSHER_GCS_KEY}/preprocessor.pkl"
            )
            
            model_pusher_artifact = ModelPusherArtifact(
                is_model_pushed=True,
                export_model_file_path=f"{MODEL_PUSHER_GCS_KEY}/model.pkl",
                export_preprocessor_file_path=f"{MODEL_PUSHER_GCS_KEY}/preprocessor.pkl"
            )
            
            logging.info("Model pushed to Google Cloud Storage successfully")
            logging.info("Exited initiate_model_pusher method of ModelPusher class")
            
            return model_pusher_artifact
            
        except Exception as e:
            raise USvisaException(e, sys)