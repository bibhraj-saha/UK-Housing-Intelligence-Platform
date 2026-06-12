"""
Crime Analytics
"""

import pandas as pd


def min_max_normalize(series):
    return (
        (series - series.min())
        /
        (series.max() - series.min())
    ) * 100


def create_crime_score(area_df):

    area_df["crime_score_v2"] = (
        100 -
        min_max_normalize(
            area_df["average_crime"]
        )
    )

    return area_df