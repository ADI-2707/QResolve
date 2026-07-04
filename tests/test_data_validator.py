import pandas as pd
import pytest

from src.data_validator import (
    validate_columns,
    validate_missing_values,
    validate_duplicate_ticket_ids,
    validate_priority_values,
    validate_department_values,
    validate_dataframe,
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


def test_validate_priority_values_passes():
    dataframe = pd.DataFrame(
        {
            "ticket_id": [1, 2, 3],
            "subject": ["A", "B", "C"],
            "description": ["A", "B", "C"],
            "priority": ["High", "Medium", "Low"],
            "department": ["IT", "Billing", "Engineering"],
        }
    )

    validate_priority_values(dataframe)


def test_validate_priority_values_fails():
    dataframe = pd.DataFrame(
        {
            "ticket_id": [1],
            "subject": ["A"],
            "description": ["A"],
            "priority": ["Urgent"],
            "department": ["IT"],
        }
    )

    with pytest.raises(ValueError):
        validate_priority_values(dataframe)


def test_validate_department_values_passes():
    dataframe = pd.DataFrame(
        {
            "ticket_id": [1, 2, 3, 4],
            "subject": ["A", "B", "C", "D"],
            "description": ["A", "B", "C", "D"],
            "priority": ["High", "Medium", "Low", "High"],
            "department": [
                "IT",
                "Billing",
                "Engineering",
                "Product",
            ],
        }
    )

    validate_department_values(dataframe)


def test_validate_department_values_fails():
    dataframe = pd.DataFrame(
        {
            "ticket_id": [1],
            "subject": ["A"],
            "description": ["A"],
            "priority": ["High"],
            "department": ["Finance"],
        }
    )

    with pytest.raises(ValueError):
        validate_department_values(dataframe)


def test_validate_dataframe_passes():
    dataframe = pd.DataFrame(
        {
            "ticket_id": [1, 2],
            "subject": ["Login", "Payment"],
            "description": [
                "Unable to login",
                "Payment failed",
            ],
            "priority": ["High", "Medium"],
            "department": ["IT", "Billing"],
        }
    )

    validate_dataframe(dataframe)


def test_validate_dataframe_fails():
    dataframe = pd.DataFrame(
        {
            "ticket_id": [1, 1],
            "subject": ["Login", "Payment"],
            "description": [
                "Unable to login",
                "Payment failed",
            ],
            "priority": ["High", "Medium"],
            "department": ["IT", "Billing"],
        }
    )

    with pytest.raises(ValueError):
        validate_dataframe(dataframe)