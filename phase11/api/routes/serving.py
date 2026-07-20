from fastapi import APIRouter, HTTPException

from phase11.services.serving_data_service import (
    ServingDataService,
)

router = APIRouter(
    prefix="/serving",
    tags=["Serving"],
)

service = ServingDataService()


@router.get("/health")
def serving_health():

    df = service.get_all()

    return {
        "status": "ready",
        "rows": len(df),
    }


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