from phase11.services.model_loader import ModelLoader


class ForecastService:

    def __init__(self):
        self.model_loader = ModelLoader()

    def forecast(self, features: dict):

        return {
            "service": "forecast",
            "status": "ready",
            "forecast": None,
            "features": features,
        }