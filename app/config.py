from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

API_TITLE = "QResolve API"
API_DESCRIPTION = "AI-powered Support Ticket Priority Prediction API"
API_VERSION = "1.0.0"

MODELS_DIR = BASE_DIR / "models"