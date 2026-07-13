from fastapi import FastAPI

from app.config import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
)
from app.schemas import TicketRequest, PredictionResponse
from app.predictor import predict_priority
from app.logger import logger

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)

logger.info("QResolve API started")


@app.get("/")
def root():
    logger.info("Root endpoint accessed")

    return {
        "message": "Welcome to QResolve API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():
    logger.info("Health check requested")

    return {
        "status": "healthy"
    }


@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(ticket: TicketRequest):
    logger.info("Prediction request received")

    prediction = predict_priority(
        ticket.model_dump()
    )

    logger.info(f"Prediction completed: {prediction}")

    return PredictionResponse(
        priority=prediction
    )