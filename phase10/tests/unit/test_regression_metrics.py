"""Tests for regression metrics."""

from __future__ import annotations

import pytest

from uk_housing_ml.evaluation.regression import (
    calculate_regression_metrics,
)


def test_perfect_predictions_have_zero_error(
) -> None:
    metrics = (
        calculate_regression_metrics(
            y_true=[
                1.0,
                2.0,
                3.0,
            ],
            y_pred=[
                1.0,
                2.0,
                3.0,
            ],
        )
    )

    assert metrics["mae"] == pytest.approx(
        0.0
    )

    assert metrics["rmse"] == pytest.approx(
        0.0
    )

    assert metrics["r2"] == pytest.approx(
        1.0
    )


def test_metric_shapes_must_match(
) -> None:
    with pytest.raises(
        ValueError,
        match="same shape",
    ):
        calculate_regression_metrics(
            y_true=[
                1.0,
                2.0,
            ],
            y_pred=[
                1.0,
            ],
        )


def test_empty_metrics_are_rejected(
) -> None:
    with pytest.raises(
        ValueError,
        match="empty",
    ):
        calculate_regression_metrics(
            y_true=[],
            y_pred=[],
        )