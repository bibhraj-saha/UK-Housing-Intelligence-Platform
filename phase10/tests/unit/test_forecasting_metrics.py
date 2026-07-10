"""Tests for forecasting metrics."""

import pytest

from uk_housing_ml.forecasting.metrics import (
    calculate_forecasting_metrics,
)


def test_perfect_forecast_has_zero_error() -> None:
    metrics = calculate_forecasting_metrics(
        [
            100.0,
            200.0,
            300.0,
        ],
        [
            100.0,
            200.0,
            300.0,
        ],
    )

    assert metrics[
        "mae"
    ] == 0.0

    assert metrics[
        "rmse"
    ] == 0.0

    assert metrics[
        "mape"
    ] == 0.0

    assert metrics[
        "r2"
    ] == 1.0


def test_forecasting_metric_shapes_must_match() -> None:
    with pytest.raises(
        ValueError,
        match="shapes must match",
    ):
        calculate_forecasting_metrics(
            [
                100.0,
                200.0,
            ],
            [
                100.0,
            ],
        )


def test_empty_forecasting_metrics_are_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="at least one observation",
    ):
        calculate_forecasting_metrics(
            [],
            [],
        )