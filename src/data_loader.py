from pathlib import Path

import pandas as pd

from src.logger import get_logger

logger = get_logger(__name__)


def load_csv(file_path: str | Path) -> pd.DataFrame:
    file_path = Path(file_path)

    if not file_path.exists():
        logger.error("File not found: %s", file_path)
        raise FileNotFoundError(file_path)

    logger.info("Loading dataset: %s", file_path)

    dataframe = pd.read_csv(file_path)

    logger.info(
        "Dataset loaded successfully (%d rows, %d columns)",
        dataframe.shape[0],
        dataframe.shape[1],
    )

    return dataframe