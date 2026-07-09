"""Tests for the model factory."""

from __future__ import annotations

import pytest
from sklearn.pipeline import Pipeline

from uk_housing_ml.models.baselines import (
    MeanRegressor,
    NaiveFeatureRegressor,
)
from uk_housing_ml.models.factory import (
    build_model,
)


def test_factory_builds_mean_baseline(
) -> None:
    model = build_model(
        model_name="mean_baseline",
        model_config={
            "parameters": {},
        },
    )

    assert isinstance(
        model,
        MeanRegressor,
    )


def test_factory_builds_naive_baseline(
) -> None:
    model = build_model(
        model_name=(
            "naive_feature_baseline"
        ),
        model_config={
            "parameters": {
                "feature_name": (
                    "price_lag_1m"
                ),
            },
        },
    )

    assert isinstance(
        model,
        NaiveFeatureRegressor,
    )


def test_factory_builds_ridge_pipeline(
) -> None:
    model = build_model(
        model_name="ridge_regression",
        model_config={
            "parameters": {
                "alpha": 1.0,
            },
        },
    )

    assert isinstance(
        model,
        Pipeline,
    )


def test_unknown_model_is_rejected(
) -> None:
    with pytest.raises(
        ValueError,
        match="Unknown model",
    ):
        build_model(
            model_name="unknown_model",
            model_config={},
        )