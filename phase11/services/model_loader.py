from pathlib import Path


class ModelLoader:
    """
    Loads trained ML models.

    Actual model loading will be implemented
    during the integration step.
    """

    def __init__(self):
        self.models_directory = Path("phase10/models")

    def load_price_model(self):
        return None

    def load_growth_model(self):
        return None

    def load_recommendation_model(self):
        return None