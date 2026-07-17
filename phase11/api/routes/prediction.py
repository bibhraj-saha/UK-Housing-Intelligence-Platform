from fastapi import APIRouter


router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"],
)


@router.post("")
def predict():
    return {
        "message": "Prediction endpoint is ready.",
        "prediction": None,
    }