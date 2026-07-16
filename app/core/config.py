from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

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

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./qresolve.db",
)

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "CHANGE_THIS_SECRET_KEY",
)

JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256",
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        60,
    )
)

MODELS_DIR = BASE_DIR / "artifacts"

LOGS_DIR = BASE_DIR / "logs"

API_CONTACT = {
    "name": "Aditya Singh",
    "email": "aditya21singh2707@gmail.com",
}

API_LICENSE = {
    "name": "MIT License",
}

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