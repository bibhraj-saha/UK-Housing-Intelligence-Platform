"""Train and evaluate forecasting models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

import pandas as pd

from uk_housing_ml.forecasting.metrics import (
    calculate_forecasting_metrics,
)
from uk_housing_ml.forecasting.model_factory import (
    build_forecasting_model,
)


@dataclass(frozen=True)
class ForecastModelResult:
    """Forecast model training result."""

    model_name: str
    model: Any
    metrics: dict[str, float | int]
    predictions: pd.Series


def train_forecasting_model(
    *,
    model_name: str,
    train_frame: pd.DataFrame,
    evaluation_frame: pd.DataFrame,
    feature_columns: Sequence[str],
    target_column: str,
    random_state: int = 42,
    naive_feature_column: str = (
        "price_lag_1m"
    ),
    model_parameters: dict[str, Any] | None = None,
) -> ForecastModelResult:
    """Train a forecasting model and evaluate it."""

    resolved_features = list(
        feature_columns
    )

    required_columns = [
        *resolved_features,
        target_column,
    ]

    for frame_name, frame in [
        (
            "train",
            train_frame,
        ),
        (
            "evaluation",
            evaluation_frame,
        ),
    ]:
        missing_columns = [
            column
            for column in required_columns
            if column not in frame.columns
        ]

        if missing_columns:
            raise ValueError(
                f"{frame_name} frame is missing "
                f"columns: {missing_columns}"
            )

    model = build_forecasting_model(
        model_name,
        random_state=random_state,
        naive_feature_column=(
            naive_feature_column
        ),
        model_parameters=(
            model_parameters
        ),
    )

    train_features = train_frame[
        resolved_features
    ]

    train_target = train_frame[
        target_column
    ]

    evaluation_features = (
        evaluation_frame[
            resolved_features
        ]
    )

    evaluation_target = (
        evaluation_frame[
            target_column
        ]
    )

    model.fit(
        train_features,
        train_target,
    )

    prediction_values = model.predict(
        evaluation_features
    )

    predictions = pd.Series(
        prediction_values,
        index=evaluation_frame.index,
        name="prediction",
        dtype=float,
    )

    metrics = calculate_forecasting_metrics(
        evaluation_target.to_numpy(),
        predictions.to_numpy(),
    )

    return ForecastModelResult(
        model_name=model_name,
        model=model,
        metrics=metrics,
        predictions=predictions,
    )