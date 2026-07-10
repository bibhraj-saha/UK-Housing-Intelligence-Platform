"""Tests for investment model factory."""

import pytest
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import Pipeline

from uk_housing_ml.investment.model_factory import (
    build_investment_model,
)


def test_factory_builds_majority_baseline() -> None:
    model = build_investment_model(
        "majority_baseline"
    )

    assert isinstance(
        model,
        DummyClassifier,
    )


def test_factory_builds_logistic_pipeline() -> None:
    model = build_investment_model(
        "logistic_regression"
    )

    assert isinstance(
        model,
        Pipeline,
    )


def test_factory_builds_random_forest_pipeline() -> None:
    model = build_investment_model(
        "random_forest"
    )

    assert isinstance(
        model,
        Pipeline,
    )


def test_unknown_investment_model_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Unknown investment model",
    ):
        build_investment_model(
            "unknown_model"
        )