"""
Investment Analytics
"""

import pandas as pd


def percentile_score(series):

    return (
        series.rank(pct=True)
        * 100
    )