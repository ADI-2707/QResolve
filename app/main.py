import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from app.config import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    API_CONTACT,
    API_LICENSE,
    API_TAGS,
)
from app.exceptions import (
    validation_exception_handler,
    generic_exception_handler,
)
from app.logger import logger
from app.predictor import predict_priority
from app.schemas import (
    TicketRequest,
    PredictionResponse,
)

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    contact=API_CONTACT,
    license_info=API_LICENSE,
    openapi_tags=API_TAGS,
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


@app.get(
    "/",
    tags=["General"],
    summary="API Home",
    description="Returns basic information about the QResolve API.",
)
def root():
    logger.info("Root endpoint accessed")

    return {
        "message": "Welcome to QResolve API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get(
    "/health",
    tags=["General"],
    summary="Health Check",
    description="Returns the current health status of the API.",
)
def health():
    logger.info("Health check requested")

    return {
        "status": "healthy",
    }


@app.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["Prediction"],
    summary="Predict Ticket Priority",
    description=(
        "Predicts the priority of a customer support ticket "
        "using the trained machine learning model."
    ),
)
def predict(ticket: TicketRequest):
    logger.info("Prediction request received")

    prediction = predict_priority(ticket.model_dump())

    logger.info(f"Prediction completed: {prediction}")

    return PredictionResponse(
        priority=prediction
    )