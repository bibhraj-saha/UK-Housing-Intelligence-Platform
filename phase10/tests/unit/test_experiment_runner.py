"""Tests for experiment runner behavior."""

from __future__ import annotations

import pandas as pd

from uk_housing_ml.training.experiment_runner import (
    _build_prediction_frame,
)


def test_prediction_frame_contains_errors(
) -> None:
    source_frame = pd.DataFrame(
        {
            "lsoa_code": [
                "A",
                "B",
            ],
            "timestamp": pd.to_datetime(
                [
                    "2026-01-31",
                    "2026-02-28",
                ]
            ),
            "future_price": [
                100.0,
                200.0,
            ],
        }
    )

    result = _build_prediction_frame(
        source_frame=source_frame,
        predictions=[
            90.0,
            220.0,
        ],
        target_column="future_price",
        model_name="test_model",
        identifier_columns=[
            "lsoa_code",
            "timestamp",
        ],
    )

    assert result[
        "residual"
    ].tolist() == [
        10.0,
        -20.0,
    ]

    assert result[
        "absolute_error"
    ].tolist() == [
        10.0,
        20.0,
    ]

    assert result[
        "model_name"
    ].tolist() == [
        "test_model",
        "test_model",
    ]