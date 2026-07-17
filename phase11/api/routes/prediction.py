from fastapi import APIRouter
from pydantic import BaseModel

from phase11.services import PredictionService


router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"],
)


prediction_service = PredictionService()


class PredictionRequest(BaseModel):

    average_price: float

    average_crime: float

    average_income: float


@router.post("")
def predict(request: PredictionRequest):

    return prediction_service.predict(
        request.model_dump()
    )