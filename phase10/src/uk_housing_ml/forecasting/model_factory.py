"""Forecasting model factory."""

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
from sklearn.preprocessing import (
    StandardScaler,
)


class MeanForecastBaseline:
    """Predict the training target mean."""

    def __init__(self) -> None:
        self.mean_: float | None = None

    def fit(
        self,
        features: Any,
        target: Any,
    ) -> "MeanForecastBaseline":
        del features

        self.mean_ = float(
            target.mean()
        )

        return self

    def predict(
        self,
        features: Any,
    ) -> Any:
        if self.mean_ is None:
            raise ValueError(
                "Model has not been fitted."
            )

        import numpy as np

        return np.full(
            len(
                features
            ),
            self.mean_,
            dtype=float,
        )


class NaiveLastValueBaseline:
    """Use the configured current-value feature."""

    def __init__(
        self,
        feature_column: str,
    ) -> None:
        self.feature_column = (
            feature_column
        )

    def fit(
        self,
        features: Any,
        target: Any,
    ) -> "NaiveLastValueBaseline":
        del target

        if self.feature_column not in features.columns:
            raise ValueError(
                "Naive baseline feature is missing: "
                f"{self.feature_column}"
            )

        return self

    def predict(
        self,
        features: Any,
    ) -> Any:
        if self.feature_column not in features.columns:
            raise ValueError(
                "Naive baseline feature is missing: "
                f"{self.feature_column}"
            )

        return (
            features[
                self.feature_column
            ]
            .to_numpy(
                dtype=float
            )
        )


def build_forecasting_model(
    model_name: str,
    *,
    random_state: int = 42,
    naive_feature_column: str = (
        "price_lag_1m"
    ),
    model_parameters: dict[str, Any] | None = None,
) -> Any:
    """Build a forecasting model."""

    parameters = dict(
        model_parameters
        or {}
    )

    if model_name == "mean_baseline":
        return MeanForecastBaseline()

    if model_name == "naive_last_value":
        return NaiveLastValueBaseline(
            feature_column=(
                naive_feature_column
            ),
        )

    if model_name == "linear_regression":
        return Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(
                        strategy="median"
                    ),
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
        alpha = float(
            parameters.pop(
                "alpha",
                1.0,
            )
        )

        return Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(
                        strategy="median"
                    ),
                ),
                (
                    "scaler",
                    StandardScaler(),
                ),
                (
                    "model",
                    Ridge(
                        alpha=alpha,
                        **parameters,
                    ),
                ),
            ]
        )

    if model_name == "random_forest":
        defaults: dict[str, Any] = {
            "n_estimators": 100,
            "max_depth": 16,
            "min_samples_leaf": 5,
            "n_jobs": -1,
            "random_state": random_state,
        }

        defaults.update(
            parameters
        )

        return Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(
                        strategy="median"
                    ),
                ),
                (
                    "model",
                    RandomForestRegressor(
                        **defaults
                    ),
                ),
            ]
        )

    raise ValueError(
        "Unknown forecasting model: "
        f"{model_name}"
    )