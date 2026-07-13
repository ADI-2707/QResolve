from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# API
API_TITLE = "QResolve API"
API_DESCRIPTION = "AI-powered Support Ticket Priority Prediction API"
API_VERSION = "1.0.0"

# Server
HOST = "0.0.0.0"
PORT = 8000

# Logging
LOG_LEVEL = "INFO"

# Paths
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"