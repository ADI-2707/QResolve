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


def validate_columns(
    dataframe: pd.DataFrame,
    required_columns: Iterable[str] = REQUIRED_COLUMNS,
) -> None:
    """
    Validate that all required columns exist.
    """

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        logger.error("Missing required columns: %s", missing_columns)
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    logger.info("All required columns are present.")


def validate_missing_values(
    dataframe: pd.DataFrame,
    required_columns: Iterable[str] = REQUIRED_COLUMNS,
) -> None:
    """
    Validate that required columns do not contain missing values.
    """

    missing = dataframe[list(required_columns)].isnull().sum()

    missing = missing[missing > 0]

    if not missing.empty:
        logger.error("Missing values detected:\n%s", missing)
        raise ValueError(
            f"Missing values detected:\n{missing}"
        )

    logger.info("No missing values found.")