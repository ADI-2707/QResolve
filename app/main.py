import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from app.api.organization import router as organization_router

from app.db.database import (
    SessionLocal,
)

import app.models

from app.core.config import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    API_CONTACT,
    API_LICENSE,
    API_TAGS,
)

from app.core.exceptions import (
    validation_exception_handler,
    generic_exception_handler,
)

from app.core.logger import logger

from app.predictor import predict_priority

from app.schemas import (
    TicketRequest,
    PredictionResponse,
    PredictionHistoryResponse,
)

from app.models import Prediction


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(
        "QResolve API started"
    )

    yield

    logger.info(
        "QResolve API shutdown"
    )


app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    contact=API_CONTACT,
    license_info=API_LICENSE,
    openapi_tags=API_TAGS,
    lifespan=lifespan,
)

app.include_router(
    organization_router
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)


app.add_exception_handler(
    Exception,
    generic_exception_handler,
)



@app.middleware("http")
async def log_requests(
    request: Request,
    call_next,
):

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"{request.method} "
        f"{request.url.path} "
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

    logger.info(
        "Root endpoint accessed"
    )

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

    logger.info(
        "Health check requested"
    )

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
def predict(
    ticket: TicketRequest,
):

    logger.info(
        "Prediction request received"
    )


    # ML Prediction

    prediction = predict_priority(
        ticket.model_dump()
    )


    logger.info(
        f"Prediction completed: {prediction}"
    )


    # Save prediction

    db = SessionLocal()

    try:

        prediction_record = Prediction(
            text=ticket.text,
            type=ticket.type,
            queue=ticket.queue,
            tag_1=ticket.tag_1,
            tag_2=ticket.tag_2,
            tag_3=ticket.tag_3,
            tag_4=ticket.tag_4,
            predicted_priority=prediction,
        )


        db.add(
            prediction_record
        )

        db.commit()

        db.refresh(
            prediction_record
        )


        logger.info(
            f"Prediction saved with ID: "
            f"{prediction_record.id}"
        )


    except Exception as e:

        db.rollback()

        logger.exception(
            f"Database error: {e}"
        )

        raise


    finally:

        db.close()


    return PredictionResponse(
        priority=prediction
    )


@app.get(
    "/predictions",
    response_model=list[PredictionHistoryResponse],
    tags=["Prediction"],
    summary="Get Prediction History",
    description=(
        "Returns previously generated ticket priority predictions."
    ),
)
def get_predictions():

    logger.info(
        "Prediction history requested"
    )


    db = SessionLocal()

    try:

        predictions = (
            db.query(Prediction)
            .order_by(
                Prediction.created_at.desc()
            )
            .all()
        )

        return predictions


    finally:

        db.close()