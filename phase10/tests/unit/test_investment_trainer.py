"""Tests for investment model training."""

import pandas as pd
import pytest

from uk_housing_ml.investment.model_factory import (
    build_investment_model,
)
from uk_housing_ml.investment.trainer import (
    train_investment_model,
)


def test_train_investment_model_returns_metrics() -> None:
    train_frame = pd.DataFrame(
        {
            "feature_a": [
                0.0,
                1.0,
                0.2,
                0.8,
                0.1,
                0.9,
            ],
            "investment_opportunity": [
                0,
                1,
                0,
                1,
                0,
                1,
            ],
        }
    )

    evaluation_frame = pd.DataFrame(
        {
            "feature_a": [
                0.15,
                0.85,
            ],
            "investment_opportunity": [
                0,
                1,
            ],
        }
    )

    model = build_investment_model(
        "logistic_regression"
    )

    result = train_investment_model(
        model,
        train_frame=train_frame,
        evaluation_frame=evaluation_frame,
        feature_columns=[
            "feature_a",
        ],
        target_column=(
            "investment_opportunity"
        ),
    )

    assert (
        result.metrics[
            "evaluated_rows"
        ]
        == 2
    )

    assert len(
        result.predictions
    ) == 2

    assert len(
        result.probabilities
    ) == 2


def test_train_investment_model_rejects_missing_columns() -> None:
    frame = pd.DataFrame(
        {
            "investment_opportunity": [
                0,
                1,
            ]
        }
    )

    model = build_investment_model(
        "majority_baseline"
    )

    with pytest.raises(
        ValueError,
        match="Missing training columns",
    ):
        train_investment_model(
            model,
            train_frame=frame,
            evaluation_frame=frame,
            feature_columns=[
                "missing_feature",
            ],
            target_column=(
                "investment_opportunity"
            ),
        )