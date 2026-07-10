"""Tests for forecasting model factory."""

import pytest
from sklearn.pipeline import Pipeline

from uk_housing_ml.forecasting.model_factory import (
    MeanForecastBaseline,
    NaiveLastValueBaseline,
    build_forecasting_model,
)


def test_factory_builds_mean_forecast_baseline() -> None:
    model = build_forecasting_model(
        "mean_baseline"
    )

    assert isinstance(
        model,
        MeanForecastBaseline,
    )


def test_factory_builds_naive_last_value() -> None:
    model = build_forecasting_model(
        "naive_last_value",
        naive_feature_column=(
            "price_lag_1m"
        ),
    )

    assert isinstance(
        model,
        NaiveLastValueBaseline,
    )


def test_factory_builds_ridge_pipeline() -> None:
    model = build_forecasting_model(
        "ridge_regression"
    )

    assert isinstance(
        model,
        Pipeline,
    )


def test_factory_builds_random_forest_pipeline() -> None:
    model = build_forecasting_model(
        "random_forest"
    )

    assert isinstance(
        model,
        Pipeline,
    )


def test_unknown_forecasting_model_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Unknown forecasting model",
    ):
        build_forecasting_model(
            "unknown_model"
        )