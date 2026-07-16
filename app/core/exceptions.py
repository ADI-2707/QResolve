from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.logger import logger


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    logger.warning(
        f"Validation error on {request.url.path}: {exc.errors()}"
    )

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": exc.errors(),
        },
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        f"Unhandled exception on {request.url.path}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong.",
        },
    )