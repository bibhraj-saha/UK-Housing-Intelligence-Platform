"""Tests for forecasting model training."""

import pandas as pd
import pytest

from uk_housing_ml.forecasting.trainer import (
    train_forecasting_model,
)


def _build_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "price_lag_1m": [
                100.0,
                110.0,
                120.0,
                130.0,
                140.0,
                150.0,
            ],
            "price_growth_1m": [
                0.01,
                0.02,
                0.01,
                0.03,
                0.02,
                0.01,
            ],
            "future_average_price_3m": [
                130.0,
                140.0,
                150.0,
                160.0,
                170.0,
                180.0,
            ],
        }
    )


def test_train_forecasting_model_returns_metrics() -> None:
    frame = _build_frame()

    result = train_forecasting_model(
        model_name="ridge_regression",
        train_frame=frame.iloc[
            :4
        ].copy(),
        evaluation_frame=frame.iloc[
            4:
        ].copy(),
        feature_columns=[
            "price_lag_1m",
            "price_growth_1m",
        ],
        target_column=(
            "future_average_price_3m"
        ),
    )

    assert result.model_name == (
        "ridge_regression"
    )

    assert "rmse" in result.metrics

    assert len(
        result.predictions
    ) == 2


def test_train_forecasting_model_rejects_missing_columns() -> None:
    frame = _build_frame()

    with pytest.raises(
        ValueError,
        match="missing columns",
    ):
        train_forecasting_model(
            model_name="ridge_regression",
            train_frame=frame,
            evaluation_frame=frame,
            feature_columns=[
                "missing_feature",
            ],
            target_column=(
                "future_average_price_3m"
            ),
        )