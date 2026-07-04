from typing import Iterable

import pandas as pd

from src.logger import get_logger

logger = get_logger(__name__)

REQUIRED_COLUMNS = [
    "Ticket ID",
    "Ticket Subject",
    "Ticket Description",
    "Ticket Priority",
    "Ticket Type",
    "Ticket Status",
]

VALID_PRIORITIES = {
    "Critical",
    "High",
    "Medium",
    "Low",
}

VALID_TICKET_TYPES = {
    "Technical issue",
    "Billing inquiry",
    "Cancellation request",
    "Product inquiry",
    "Refund request",
}

VALID_STATUSES = {
    "Open",
    "Closed",
    "Pending",
    "Pending Customer Response",
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
    Validate that Ticket IDs are unique.
    """

    duplicates = dataframe["Ticket ID"].duplicated()

    if duplicates.any():
        duplicate_ids = dataframe.loc[
            duplicates,
            "Ticket ID",
        ].tolist()

        logger.error(
            "Duplicate Ticket IDs found: %s",
            duplicate_ids,
        )

        raise ValueError(
            f"Duplicate Ticket IDs found: {duplicate_ids}"
        )

    logger.info("No duplicate Ticket IDs found.")


def validate_priority_values(dataframe: pd.DataFrame) -> None:
    """
    Validate priority values.
    """

    invalid = (
        dataframe.loc[
            ~dataframe["Ticket Priority"].isin(VALID_PRIORITIES),
            "Ticket Priority",
        ]
        .dropna()
        .unique()
    )

    if len(invalid) > 0:
        logger.error(
            "Invalid priority values: %s",
            list(invalid),
        )

        raise ValueError(
            f"Invalid priority values: {list(invalid)}"
        )

    logger.info("Priority values are valid.")


def validate_ticket_type_values(dataframe: pd.DataFrame) -> None:
    """
    Validate ticket type values.
    """

    invalid = (
        dataframe.loc[
            ~dataframe["Ticket Type"].isin(VALID_TICKET_TYPES),
            "Ticket Type",
        ]
        .dropna()
        .unique()
    )

    if len(invalid) > 0:
        logger.error(
            "Invalid ticket types: %s",
            list(invalid),
        )

        raise ValueError(
            f"Invalid ticket types: {list(invalid)}"
        )

    logger.info("Ticket types are valid.")


def validate_status_values(dataframe: pd.DataFrame) -> None:
    """
    Validate ticket status values.
    """

    invalid = (
        dataframe.loc[
            ~dataframe["Ticket Status"].isin(VALID_STATUSES),
            "Ticket Status",
        ]
        .dropna()
        .unique()
    )

    if len(invalid) > 0:
        logger.error(
            "Invalid status values: %s",
            list(invalid),
        )

        raise ValueError(
            f"Invalid status values: {list(invalid)}"
        )

    logger.info("Ticket status values are valid.")


def validate_dataframe(dataframe: pd.DataFrame) -> None:
    """
    Run all validation checks.
    """

    logger.info("Starting dataset validation.")

    validate_columns(dataframe)
    validate_missing_values(dataframe)
    validate_duplicate_ticket_ids(dataframe)
    validate_priority_values(dataframe)
    validate_ticket_type_values(dataframe)
    validate_status_values(dataframe)

    logger.info("Dataset validation completed successfully.")