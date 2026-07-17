from phase11.services.model_loader import ModelLoader
from phase11.services.preprocessing import DataPreprocessor


class PredictionService:

    def __init__(self):
        self.model_loader = ModelLoader()
        self.preprocessor = DataPreprocessor()

    def predict(self, features: dict):

        processed_features = self.preprocessor.preprocess(features)

        return {
            "service": "prediction",
            "status": "ready",
            "features": processed_features,
            "prediction": None,
        }