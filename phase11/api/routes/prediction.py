from fastapi import APIRouter

from phase11.services import PredictionService


router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"],
)

prediction_service = PredictionService()


@router.post("")
def predict():

    sample_features = {
        "average_price": 300000,
        "average_crime": 45,
        "average_income": 50000,
    }

    return prediction_service.predict(sample_features)