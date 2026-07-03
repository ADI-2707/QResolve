from pathlib import Path

from src.data_loader import load_csv


def test_load_csv_returns_dataframe():
    dataframe = load_csv(Path("data/raw/sample_tickets.csv"))

    assert dataframe is not None
    assert not dataframe.empty
    assert dataframe.shape[0] == 10
    assert dataframe.shape[1] == 5