from pathlib import Path

import pandas as pd


class ServingDataService:

    def __init__(self):

        self.serving_path = Path(
            "phase10/data/serving/area_ml_serving.parquet"
        )

        self._serving_df = None

    # -----------------------------------------------------
    # DATA LOADER
    # -----------------------------------------------------

    def load(self):

        if self._serving_df is None:

            self._serving_df = pd.read_parquet(
                self.serving_path
            )

        return self._serving_df

    # -----------------------------------------------------
    # COMPLETE DATASET
    # -----------------------------------------------------

    def get_all(self):

        return self.load()

    # -----------------------------------------------------
    # AVAILABLE LSOAs
    # -----------------------------------------------------

    def list_areas(self):

        df = self.load()

        return (
            df[
                [
                    "lsoa_code"
                ]
            ]
            .drop_duplicates()
            .sort_values(
                "lsoa_code"
            )
            .reset_index(
                drop=True
            )
            .to_dict(
                orient="records"
            )
        )

    # -----------------------------------------------------
    # SINGLE AREA
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # PRICE PREDICTION
    # -----------------------------------------------------

    def get_price_prediction(
        self,
        lsoa_code: str,
    ):

        area = self.get_area(
            lsoa_code
        )

        if area is None:

            return None

        return {

            "lsoa_code":
                area["lsoa_code"],

            "timestamp":
                area["timestamp"],

            "predicted_future_price":
                area[
                    "predicted_future_price"
                ]

        }

    # -----------------------------------------------------
    # GROWTH
    # -----------------------------------------------------

    def get_growth_prediction(
        self,
        lsoa_code: str,
    ):

        area = self.get_area(
            lsoa_code
        )

        if area is None:

            return None

        return {

            "lsoa_code":
                area["lsoa_code"],

            "predicted_future_growth":
                area[
                    "predicted_future_growth"
                ]

        }

    # -----------------------------------------------------
    # INVESTMENT
    # -----------------------------------------------------

    def get_investment_prediction(
        self,
        lsoa_code: str,
    ):

        area = self.get_area(
            lsoa_code
        )

        if area is None:

            return None

        return {

            "lsoa_code":
                area["lsoa_code"],

            "opportunity_probability":
                area[
                    "opportunity_probability"
                ]

        }

    # -----------------------------------------------------
    # RECOMMENDATION
    # -----------------------------------------------------

    def get_recommendation(
        self,
        lsoa_code: str,
    ):

        area = self.get_area(
            lsoa_code
        )

        if area is None:

            return None

        return {

            "lsoa_code":
                area["lsoa_code"],

            "recommendation_rank":
                area[
                    "recommendation_rank"
                ],

            "recommendation_score":
                area[
                    "recommendation_score"
                ],

            "recommendation_percentile":
                area[
                    "recommendation_percentile"
                ]

        }