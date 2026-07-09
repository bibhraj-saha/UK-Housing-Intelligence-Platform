"""Model training utilities."""

from __future__ import annotations

from typing import Any

import pandas as pd

from uk_housing_ml.evaluation.regression import (
    calculate_regression_metrics,
)


def train_model(
    model: Any,
    train_frame: pd.DataFrame,
    evaluation_frame: pd.DataFrame,
    feature_columns: list[str],
    target_column: str,
) -> tuple[Any, dict[str, float]]:
    """Fit a model and evaluate it."""

    required_columns = set(
        feature_columns
        + [
            target_column,
        ]
    )

    for frame_name, frame in (
        (
            "train",
            train_frame,
        ),
        (
            "evaluation",
            evaluation_frame,
        ),
    ):
        missing_columns = sorted(
            required_columns
            - set(frame.columns)
        )

        if missing_columns:
            raise ValueError(
                f"{frame_name} frame is missing "
                f"columns: {missing_columns}"
            )

    X_train = train_frame[
        feature_columns
    ]

    y_train = train_frame[
        target_column
    ]

    X_evaluation = evaluation_frame[
        feature_columns
    ]

    y_evaluation = evaluation_frame[
        target_column
    ]

    model.fit(
        X_train,
        y_train,
    )

    predictions = model.predict(
        X_evaluation
    )

    metrics = (
        calculate_regression_metrics(
            y_true=y_evaluation,
            y_pred=predictions,
        )
    )

    return model, metrics