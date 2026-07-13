from pathlib import Path

from dotenv import load_dotenv

import os


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# API

API_TITLE = os.getenv(
    "API_TITLE",
    "QResolve API",
)

API_DESCRIPTION = os.getenv(
    "API_DESCRIPTION",
    "AI-powered Support Ticket Priority Prediction API",
)

API_VERSION = os.getenv(
    "API_VERSION",
    "1.0.0",
)


# Server

HOST = os.getenv(
    "HOST",
    "0.0.0.0",
)

PORT = int(
    os.getenv(
        "PORT",
        8000,
    )
)


# Logging

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)


# Paths

MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"


# Contact

API_CONTACT = {
    "name": "Aditya Singh",
    "email": "aditya21singh2707@gmail.com",
}


# License

API_LICENSE = {
    "name": "MIT License",
}


# Tags

API_TAGS = [
    {
        "name": "General",
        "description": "General application endpoints",
    },
    {
        "name": "Prediction",
        "description": "Ticket priority prediction endpoints",
    },
]