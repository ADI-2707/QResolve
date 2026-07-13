import time

from fastapi import FastAPI, Request

from app.config import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
)
from app.schemas import TicketRequest, PredictionResponse
from app.predictor import predict_priority
from app.logger import logger

from fastapi.exceptions import RequestValidationError

from app.exceptions import (
    validation_exception_handler,
    generic_exception_handler,
)

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)

logger.info("QResolve API started")

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} "
        f"{response.status_code} "
        f"{duration:.3f}s"
    )

    return response


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

    prediction = predict_priority(ticket.model_dump())

    logger.info(f"Prediction completed: {prediction}")

    return PredictionResponse(
        priority=prediction
    )