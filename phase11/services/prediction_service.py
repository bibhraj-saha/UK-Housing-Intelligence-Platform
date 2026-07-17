from phase11.services.model_loader import ModelLoader
from phase11.services.preprocessing import DataPreprocessor


class PredictionService:

    def __init__(self):

        self.model_loader = ModelLoader()

        self.preprocessor = DataPreprocessor()

    def predict(
        self,
        features: dict,
    ):

        processed = self.preprocessor.preprocess(
            features
        )

        return {
            "service": "prediction",
            "status": "ready",
            "message": (
                "ML model integration "
                "will be completed in Step 5."
            ),
            "input_features": processed,
            "prediction": None,
        }