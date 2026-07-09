"""Factory for regression models."""

from __future__ import annotations

from typing import Any

from sklearn.ensemble import (
    RandomForestRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.linear_model import (
    LinearRegression,
    Ridge,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from uk_housing_ml.models.baselines import (
    MeanRegressor,
    NaiveFeatureRegressor,
)


def build_model(
    model_name: str,
    model_config: dict[str, Any],
) -> Any:
    """Build a configured regression model."""

    parameters = dict(
        model_config.get(
            "parameters",
            {},
        )
    )

    if model_name == "mean_baseline":
        return MeanRegressor()

    if model_name == "naive_feature_baseline":
        feature_name = parameters.get(
            "feature_name"
        )

        if not feature_name:
            raise ValueError(
                "naive_feature_baseline requires "
                "'feature_name'."
            )

        return NaiveFeatureRegressor(
            feature_name=str(feature_name),
        )

    if model_name == "linear_regression":
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
                    "model",
                    LinearRegression(
                        **parameters
                    ),
                ),
            ]
        )

    if model_name == "ridge_regression":
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
                    "model",
                    Ridge(
                        **parameters
                    ),
                ),
            ]
        )

    if model_name == "random_forest":
        return Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(
                        strategy="median",
                    ),
                ),
                (
                    "model",
                    RandomForestRegressor(
                        **parameters
                    ),
                ),
            ]
        )

    raise ValueError(
        f"Unknown model name: {model_name}"
    )