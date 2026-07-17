"""Tests for feature drift detection."""

import pandas as pd

from uk_housing_ml.monitoring.drift import (
    calculate_numeric_drift,
)


def test_identical_series_has_no_drift() -> None:
    result = calculate_numeric_drift(
        reference=pd.Series(
            [
                1.0,
                2.0,
                3.0,
            ]
        ),
        current=pd.Series(
            [
                1.0,
                2.0,
                3.0,
            ]
        ),
        threshold=0.25,
    )

    assert (
        result[
            "drift_detected"
        ]
        is False
    )


def test_shifted_series_detects_drift() -> None:
    result = calculate_numeric_drift(
        reference=pd.Series(
            [
                1.0,
                2.0,
                3.0,
            ]
        ),
        current=pd.Series(
            [
                10.0,
                11.0,
                12.0,
            ]
        ),
        threshold=0.25,
    )

    assert (
        result[
            "drift_detected"
        ]
        is True
    )