"""
Ranking Engine
"""

import pandas as pd


def create_rankings(df):

    df["area_rank"] = (
        df["housing_intelligence_index"]
        .rank(
            ascending=False,
            method="dense"
        )
    )

    df["percentile_rank"] = (
        df["housing_intelligence_index"]
        .rank(pct=True)
        * 100
    )

    return df