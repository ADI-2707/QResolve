import pandas as pd
import pytest

from src.data_validator import (
    validate_columns,
    validate_missing_values,
    validate_duplicate_ticket_ids,
)


def test_validate_columns_passes():
    dataframe = pd.DataFrame(
        {
            "ticket_id": [1],
            "subject": ["Login"],
            "description": ["Unable to login"],
            "priority": ["High"],
            "department": ["IT"],
        }
    )

    validate_columns(dataframe)


def test_validate_columns_fails():
    dataframe = pd.DataFrame(
        {
            "ticket_id": [1],
            "subject": ["Login"],
        }
    )

    with pytest.raises(ValueError):
        validate_columns(dataframe)


def test_validate_missing_values_passes():
    dataframe = pd.DataFrame(
        {
            "ticket_id": [1],
            "subject": ["Login"],
            "description": ["Unable to login"],
            "priority": ["High"],
            "department": ["IT"],
        }
    )

    validate_missing_values(dataframe)


def test_validate_missing_values_fails():
    dataframe = pd.DataFrame(
        {
            "ticket_id": [1],
            "subject": [None],
            "description": ["Unable to login"],
            "priority": ["High"],
            "department": ["IT"],
        }
    )

    with pytest.raises(ValueError):
        validate_missing_values(dataframe)


def test_validate_duplicate_ticket_ids_passes():
    dataframe = pd.DataFrame(
        {
            "ticket_id": [1, 2],
            "subject": ["Login", "Payment"],
            "description": ["Unable to login", "Card declined"],
            "priority": ["High", "Medium"],
            "department": ["IT", "Billing"],
        }
    )

    validate_duplicate_ticket_ids(dataframe)


def test_validate_duplicate_ticket_ids_fails():
    dataframe = pd.DataFrame(
        {
            "ticket_id": [1, 1],
            "subject": ["Login", "Payment"],
            "description": ["Unable to login", "Card declined"],
            "priority": ["High", "Medium"],
            "department": ["IT", "Billing"],
        }
    )

    with pytest.raises(ValueError):
        validate_duplicate_ticket_ids(dataframe)