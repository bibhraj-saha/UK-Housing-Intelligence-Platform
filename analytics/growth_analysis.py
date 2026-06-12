"""
Growth Analytics
"""

import pandas as pd


def percentile_score(series):

    return (
        series.rank(pct=True)
        * 100
    )


def reverse_percentile_score(series):

    return (
        100 -
        (series.rank(pct=True) * 100)
    )