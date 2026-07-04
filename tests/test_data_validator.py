import pandas as pd
import pytest

from src.data_validator import validate_columns


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