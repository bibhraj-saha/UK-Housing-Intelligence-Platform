from fastapi import APIRouter
from fastapi import HTTPException

from phase11.services.serving_data_service import (
    ServingDataService,
)

router = APIRouter(
    prefix="/serving",
    tags=["Serving"],
)

service = ServingDataService()


# ============================================================
# HEALTH
# ============================================================

@router.get("/health")
def serving_health():

    df = service.get_all()

    return {
        "status": "ready",
        "rows": len(df),
    }


# ============================================================
# AVAILABLE AREAS
# ============================================================

@router.get("/areas")
def serving_areas():

    return service.list_areas()


# ============================================================
# COMPLETE AREA
# ============================================================

@router.get("/{lsoa_code}")
def serving_area(
    lsoa_code: str,
):

    area = service.get_area(
        lsoa_code
    )

    if area is None:

        raise HTTPException(
            status_code=404,
            detail="LSOA not found",
        )

    return area


# ============================================================
# PRICE PREDICTION
# ============================================================

@router.get("/{lsoa_code}/price")
def price_prediction(
    lsoa_code: str,
):

    prediction = service.get_price_prediction(
        lsoa_code
    )

    if prediction is None:

        raise HTTPException(
            status_code=404,
            detail="LSOA not found",
        )

    return prediction


# ============================================================
# GROWTH PREDICTION
# ============================================================

@router.get("/{lsoa_code}/growth")
def growth_prediction(
    lsoa_code: str,
):

    prediction = service.get_growth_prediction(
        lsoa_code
    )

    if prediction is None:

        raise HTTPException(
            status_code=404,
            detail="LSOA not found",
        )

    return prediction


# ============================================================
# INVESTMENT
# ============================================================

@router.get("/{lsoa_code}/investment")
def investment_prediction(
    lsoa_code: str,
):

    prediction = service.get_investment_prediction(
        lsoa_code
    )

    if prediction is None:

        raise HTTPException(
            status_code=404,
            detail="LSOA not found",
        )

    return prediction


# ============================================================
# RECOMMENDATION
# ============================================================

@router.get("/{lsoa_code}/recommendation")
def recommendation(
    lsoa_code: str,
):

    prediction = service.get_recommendation(
        lsoa_code
    )

    if prediction is None:

        raise HTTPException(
            status_code=404,
            detail="LSOA not found",
        )

    return prediction