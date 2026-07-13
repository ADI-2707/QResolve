import logging

from app.config import LOG_LEVEL, LOGS_DIR

LOGS_DIR.mkdir(exist_ok=True)

LOG_FILE = LOGS_DIR / "api.log"

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("QResolveAPI")