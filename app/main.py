from fastapi import FastAPI

from app.schemas import TicketRequest, PredictionResponse
from app.predictor import predict_priority

app = FastAPI(
    title="QResolve API",
    description="AI-powered Support Ticket Priority Prediction API",
    version="1.0.0"
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