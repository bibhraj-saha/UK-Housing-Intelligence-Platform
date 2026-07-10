"""Tests for forecasting dataset construction."""

import pandas as pd

from uk_housing_ml.forecasting.dataset_builder import (
    build_forecasting_dataset,
)


def test_forecasting_target_uses_forward_shift() -> None:
    frame = pd.DataFrame(
        {
            "lsoa_code": [
                "A",
                "A",
                "A",
                "A",
            ],
            "period_end": pd.to_datetime(
                [
                    "2025-01-31",
                    "2025-02-28",
                    "2025-03-31",
                    "2025-04-30",
                ]
            ),
            "average_price": [
                100.0,
                110.0,
                120.0,
                130.0,
            ],
            "price_lag_1m": [
                90.0,
                100.0,
                110.0,
                120.0,
            ],
        }
    )

    result = build_forecasting_dataset(
        frame,
        entity_column="lsoa_code",
        timestamp_column="period_end",
        value_column="average_price",
        feature_columns=[
            "price_lag_1m",
        ],
        horizon_months=2,
    )

    assert result.target_column == (
        "future_average_price_2m"
    )

    assert result.dataset[
        result.target_column
    ].tolist() == [
        120.0,
        130.0,
    ]


def test_forecasting_target_does_not_cross_entities() -> None:
    frame = pd.DataFrame(
        {
            "lsoa_code": [
                "A",
                "A",
                "B",
                "B",
            ],
            "period_end": pd.to_datetime(
                [
                    "2025-01-31",
                    "2025-02-28",
                    "2025-01-31",
                    "2025-02-28",
                ]
            ),
            "average_price": [
                100.0,
                110.0,
                500.0,
                550.0,
            ],
            "price_lag_1m": [
                90.0,
                100.0,
                450.0,
                500.0,
            ],
        }
    )

    result = build_forecasting_dataset(
        frame,
        entity_column="lsoa_code",
        timestamp_column="period_end",
        value_column="average_price",
        feature_columns=[
            "price_lag_1m",
        ],
        horizon_months=1,
    )

    assert result.dataset[
        result.target_column
    ].tolist() == [
        110.0,
        550.0,
    ]