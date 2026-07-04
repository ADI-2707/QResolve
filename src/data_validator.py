from typing import Iterable

import pandas as pd

from src.logger import get_logger

logger = get_logger(__name__)

REQUIRED_COLUMNS = (
    "ticket_id",
    "subject",
    "description",
    "priority",
    "department",
)