from fastapi import FastAPI

from app.config import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
)
from app.schemas import TicketRequest, PredictionResponse
from app.predictor import predict_priority

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)


@app.get("/")
def root():
    return {
        "message": "Welcome to QResolve API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(ticket: TicketRequest):

    prediction = predict_priority(
        ticket.model_dump()
    )

    return PredictionResponse(
        priority=prediction
    )