"""Tests for model training."""

from __future__ import annotations

import pandas as pd
import pytest
from sklearn.linear_model import (
    LinearRegression,
)

from uk_housing_ml.training.model_trainer import (
    train_model,
)


def test_train_model_returns_metrics(
) -> None:
    train_frame = pd.DataFrame(
        {
            "feature_a": [
                1.0,
                2.0,
                3.0,
                4.0,
            ],
            "target": [
                2.0,
                4.0,
                6.0,
                8.0,
            ],
        }
    )

    evaluation_frame = pd.DataFrame(
        {
            "feature_a": [
                5.0,
                6.0,
            ],
            "target": [
                10.0,
                12.0,
            ],
        }
    )

    _, metrics = train_model(
        model=LinearRegression(),
        train_frame=train_frame,
        evaluation_frame=(
            evaluation_frame
        ),
        feature_columns=[
            "feature_a",
        ],
        target_column="target",
    )

    assert metrics["rmse"] == pytest.approx(
        0.0
    )

    assert metrics["mae"] == pytest.approx(
        0.0
    )


def test_train_model_rejects_missing_columns(
) -> None:
    train_frame = pd.DataFrame(
        {
            "feature_a": [
                1.0,
            ],
            "target": [
                2.0,
            ],
        }
    )

    evaluation_frame = pd.DataFrame(
        {
            "target": [
                3.0,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="missing columns",
    ):
        train_model(
            model=LinearRegression(),
            train_frame=train_frame,
            evaluation_frame=(
                evaluation_frame
            ),
            feature_columns=[
                "feature_a",
            ],
            target_column="target",
        )