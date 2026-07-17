from fastapi import FastAPI

from phase11.api.routes.health import router as health_router
from phase11.api.routes.prediction import router as prediction_router
from phase11.config import settings


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="UK Housing Intelligence Platform REST API",
)

app.include_router(health_router)
app.include_router(prediction_router)


@app.get("/")
def root():
    return {
        "message": "UK Housing Intelligence Platform API",
        "environment": settings.app_env,
        "version": "1.0.0",
    }