from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "analytics"
    / "housing_intelligence.parquet"
)


def load_housing_data():
    """
    Load master housing intelligence dataset.
    """

    return pd.read_parquet(DATA_PATH)