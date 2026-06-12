"""
Affordability Analysis
"""

import pandas as pd


def create_area_level_dataset(df):
    """
    Aggregate transaction-level data
    into area-level analytics.
    """

    area_df = (
        df.groupby("lsoa_code")
        .agg(
            average_price=("price", "mean"),
            median_price=("price", "median"),
            transaction_count=("price", "count"),
            average_crime=("total_crimes", "mean"),
            average_deprivation=("deprivation_index", "mean")
        )
        .reset_index()
    )

    return area_df


def min_max_normalize(series):
    return (
        (series - series.min())
        /
        (series.max() - series.min())
    ) * 100


def create_affordability_score(area_df):

    area_df["affordability_score"] = (
        100 -
        min_max_normalize(
            area_df["median_price"]
        )
    )

    return area_df