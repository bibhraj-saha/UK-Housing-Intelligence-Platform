"""Tests for investment classification metrics."""

import pytest

from uk_housing_ml.investment.metrics import (
    calculate_classification_metrics,
)


def test_perfect_classification_metrics() -> None:
    metrics = calculate_classification_metrics(
        [
            0,
            1,
            0,
            1,
        ],
        [
            0,
            1,
            0,
            1,
        ],
        [
            0.1,
            0.9,
            0.2,
            0.8,
        ],
    )

    assert metrics[
        "accuracy"
    ] == 1.0

    assert metrics[
        "f1"
    ] == 1.0

    assert metrics[
        "roc_auc"
    ] == 1.0


def test_metric_shapes_must_match() -> None:
    with pytest.raises(
        ValueError,
        match="shapes must match",
    ):
        calculate_classification_metrics(
            [
                0,
                1,
            ],
            [
                0,
            ],
            [
                0.1,
                0.9,
            ],
        )