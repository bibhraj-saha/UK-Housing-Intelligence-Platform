"""Baseline regression models."""

from __future__ import annotations

import numpy as np
import pandas as pd


class MeanRegressor:
    """Predict the training-target mean."""

    def __init__(self) -> None:
        self.mean_: float | None = None

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> "MeanRegressor":
        del X

        if y.empty:
            raise ValueError(
                "Cannot fit MeanRegressor "
                "with an empty target."
            )

        self.mean_ = float(
            pd.to_numeric(
                y,
                errors="coerce",
            ).mean()
        )

        if not np.isfinite(self.mean_):
            raise ValueError(
                "Target mean is not finite."
            )

        return self

    def predict(
        self,
        X: pd.DataFrame,
    ) -> np.ndarray:
        if self.mean_ is None:
            raise RuntimeError(
                "MeanRegressor must be fitted "
                "before prediction."
            )

        return np.full(
            shape=len(X),
            fill_value=self.mean_,
            dtype=float,
        )


class NaiveFeatureRegressor:
    """Predict directly from one historical feature."""

    def __init__(
        self,
        feature_name: str,
    ) -> None:
        self.feature_name = feature_name
        self.is_fitted_: bool = False

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> "NaiveFeatureRegressor":
        del y

        if self.feature_name not in X.columns:
            raise ValueError(
                "Naive baseline feature "
                f"'{self.feature_name}' "
                "was not found."
            )

        self.is_fitted_ = True

        return self

    def predict(
        self,
        X: pd.DataFrame,
    ) -> np.ndarray:
        if not self.is_fitted_:
            raise RuntimeError(
                "NaiveFeatureRegressor must "
                "be fitted before prediction."
            )

        if self.feature_name not in X.columns:
            raise ValueError(
                "Naive baseline feature "
                f"'{self.feature_name}' "
                "was not found."
            )

        values = pd.to_numeric(
            X[self.feature_name],
            errors="coerce",
        )

        return values.to_numpy(
            dtype=float,
        )