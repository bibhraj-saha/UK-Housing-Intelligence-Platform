from pathlib import Path

import pandas as pd


class ServingDataService:

    def __init__(self):

        self.serving_path = Path(
            "phase10/data/serving/area_ml_serving.parquet"
        )

        self._serving_df = None

    def load(self):

        if self._serving_df is None:

            self._serving_df = pd.read_parquet(
                self.serving_path
            )

        return self._serving_df

    def get_all(self):

        return self.load()

    def get_area(
        self,
        lsoa_code: str,
    ):

        df = self.load()

        result = df[
            df["lsoa_code"] == lsoa_code
        ]

        if result.empty:

            return None

        return result.iloc[0].to_dict()