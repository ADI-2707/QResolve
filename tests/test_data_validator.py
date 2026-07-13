import pandas as pd
import pytest

from src.data_validator import (
    validate_columns,
    validate_missing_values,
    validate_duplicate_ticket_ids,
    validate_priority_values,
    validate_ticket_type_values,
    validate_status_values,
    validate_dataframe,
)


def valid_dataframe():
    return pd.DataFrame(
        {
            "Ticket ID": [1, 2],
            "Ticket Subject": ["Login", "Payment"],
            "Ticket Description": [
                "Unable to login",
                "Card declined",
            ],
            "Ticket Priority": [
                "High",
                "Medium",
            ],
            "Ticket Type": [
                "Technical issue",
                "Billing inquiry",
            ],
            "Ticket Status": [
                "Open",
                "Closed",
            ],
        }
    )


def test_validate_columns_passes():
    validate_columns(valid_dataframe())


def test_validate_columns_fails():
    dataframe = valid_dataframe().drop(
        columns=["Ticket Status"]
    )

    with pytest.raises(ValueError):
        validate_columns(dataframe)


def test_validate_missing_values_passes():
    validate_missing_values(valid_dataframe())


def test_validate_missing_values_fails():
    dataframe = valid_dataframe()

    dataframe.loc[0, "Ticket Subject"] = None

    with pytest.raises(ValueError):
        validate_missing_values(dataframe)


def test_validate_duplicate_ticket_ids_passes():
    validate_duplicate_ticket_ids(valid_dataframe())


def test_validate_duplicate_ticket_ids_fails():
    dataframe = valid_dataframe()

    dataframe.loc[1, "Ticket ID"] = 1

    with pytest.raises(ValueError):
        validate_duplicate_ticket_ids(dataframe)


def test_validate_priority_values_passes():
    validate_priority_values(valid_dataframe())


def test_validate_priority_values_fails():
    dataframe = valid_dataframe()

    dataframe.loc[0, "Ticket Priority"] = "Urgent"

    with pytest.raises(ValueError):
        validate_priority_values(dataframe)


def test_validate_ticket_type_values_passes():
    validate_ticket_type_values(valid_dataframe())


def test_validate_ticket_type_values_fails():
    dataframe = valid_dataframe()

    dataframe.loc[0, "Ticket Type"] = "Finance"

    with pytest.raises(ValueError):
        validate_ticket_type_values(dataframe)


def test_validate_status_values_passes():
    validate_status_values(valid_dataframe())


def test_validate_status_values_fails():
    dataframe = valid_dataframe()

    dataframe.loc[0, "Ticket Status"] = "Resolved"

    with pytest.raises(ValueError):
        validate_status_values(dataframe)


def test_validate_dataframe_passes():
    validate_dataframe(valid_dataframe())


def test_validate_dataframe_fails():
    dataframe = valid_dataframe()

    dataframe.loc[1, "Ticket ID"] = 1

    with pytest.raises(ValueError):
        validate_dataframe(dataframe)