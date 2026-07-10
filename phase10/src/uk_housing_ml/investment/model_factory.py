"""Classifier factory for investment opportunity models."""

from __future__ import annotations

from typing import Any

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_investment_model(
    model_name: str,
    *,
    random_state: int = 42,
    model_parameters: dict[str, Any] | None = None,
) -> Any:
    """Build a configured investment classifier."""

    parameters = dict(
        model_parameters
        if model_parameters is not None
        else {}
    )

    if model_name == "majority_baseline":
        return DummyClassifier(
            strategy="most_frequent",
        )

    if model_name == "logistic_regression":
        classifier_parameters = {
            "max_iter": 1000,
            "random_state": random_state,
        }

        classifier_parameters.update(
            parameters
        )

        return Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(
                        strategy="median",
                    ),
                ),
                (
                    "scaler",
                    StandardScaler(),
                ),
                (
                    "classifier",
                    LogisticRegression(
                        **classifier_parameters
                    ),
                ),
            ]
        )

    if model_name == "random_forest":
        classifier_parameters = {
            "n_estimators": 100,
            "max_depth": 12,
            "min_samples_leaf": 5,
            "n_jobs": -1,
            "random_state": random_state,
        }

        classifier_parameters.update(
            parameters
        )

        return Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(
                        strategy="median",
                    ),
                ),
                (
                    "classifier",
                    RandomForestClassifier(
                        **classifier_parameters
                    ),
                ),
            ]
        )

    raise ValueError(
        f"Unknown investment model: {model_name}"
    )