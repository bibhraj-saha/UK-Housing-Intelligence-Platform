"""
Housing Intelligence Index
"""

import pandas as pd


def calculate_housing_intelligence_index(df):

    df["housing_intelligence_index"] = (
        df["affordability_score"] * 0.25
        +
        df["crime_score"] * 0.20
        +
        df["growth_score"] * 0.25
        +
        df["investment_score"] * 0.30
    )

    return df