from fastapi import FastAPI

from app.schemas import TicketRequest, PredictionResponse
from app.predictor import predict_priority


app = FastAPI(
    title="QResolve Ticket Priority API",
    version="1.0.0",
    description="Production Support Ticket Priority Prediction API"
)


@app.get("/")
def root():
    return {
        "message": "QResolve API is running."
    }


@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(request: TicketRequest):

    prediction = predict_priority(
        request.model_dump()
    )

    return PredictionResponse(
        priority=prediction
    )