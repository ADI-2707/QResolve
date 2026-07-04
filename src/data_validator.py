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

VALID_PRIORITIES = {
    "High",
    "Medium",
    "Low",
}

VALID_DEPARTMENTS = {
    "IT",
    "Billing",
    "Engineering",
    "Product",
}


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


def validate_duplicate_ticket_ids(dataframe: pd.DataFrame) -> None:
    """
    Validate that ticket IDs are unique.
    """

    duplicates = dataframe["ticket_id"].duplicated()

    if duplicates.any():
        duplicate_ids = dataframe.loc[duplicates, "ticket_id"].tolist()

        logger.error("Duplicate ticket IDs found: %s", duplicate_ids)

        raise ValueError(
            f"Duplicate ticket IDs found: {duplicate_ids}"
        )

    logger.info("No duplicate ticket IDs found.")


def validate_priority_values(dataframe: pd.DataFrame) -> None:
    """
    Validate that the priority column contains only valid values.
    """

    invalid_priorities = (
        dataframe.loc[
            ~dataframe["priority"].isin(VALID_PRIORITIES),
            "priority",
        ]
        .dropna()
        .unique()
    )

    if len(invalid_priorities) > 0:
        logger.error(
            "Invalid priority values found: %s",
            list(invalid_priorities),
        )

        raise ValueError(
            f"Invalid priority values: {list(invalid_priorities)}"
        )

    logger.info("Priority values are valid.")


def validate_department_values(dataframe: pd.DataFrame) -> None:
    """
    Validate that the department column contains only valid values.
    """

    invalid_departments = (
        dataframe.loc[
            ~dataframe["department"].isin(VALID_DEPARTMENTS),
            "department",
        ]
        .dropna()
        .unique()
    )

    if len(invalid_departments) > 0:
        logger.error(
            "Invalid department values found: %s",
            list(invalid_departments),
        )

        raise ValueError(
            f"Invalid department values: {list(invalid_departments)}"
        )

    logger.info("Department values are valid.")


def validate_dataframe(dataframe: pd.DataFrame) -> None:
    """
    Run all validation checks on the dataset.
    """

    logger.info("Starting dataset validation.")

    validate_columns(dataframe)
    validate_missing_values(dataframe)
    validate_duplicate_ticket_ids(dataframe)
    validate_priority_values(dataframe)
    validate_department_values(dataframe)

    logger.info("Dataset validation completed successfully.")