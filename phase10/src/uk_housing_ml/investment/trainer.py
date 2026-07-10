"""Training utilities for investment classifiers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from uk_housing_ml.investment.metrics import (
    calculate_classification_metrics,
)


@dataclass(frozen=True)
class InvestmentTrainingResult:
    """Result from training one investment classifier."""

    model: Any
    metrics: dict[str, float | int | None]
    predictions: np.ndarray
    probabilities: np.ndarray


def _validate_columns(
    frame: pd.DataFrame,
    *,
    feature_columns: list[str],
    target_column: str,
) -> None:
    required = {
        *feature_columns,
        target_column,
    }

    missing = sorted(
        required.difference(
            frame.columns
        )
    )

    if missing:
        raise ValueError(
            "Missing training columns: "
            f"{missing}"
        )


def _positive_class_probability(
    model: Any,
    features: pd.DataFrame,
) -> np.ndarray:
    if not hasattr(
        model,
        "predict_proba",
    ):
        return np.asarray(
            model.predict(
                features
            ),
            dtype=float,
        )

    probabilities = model.predict_proba(
        features
    )

    classes = np.asarray(
        model.classes_
    )

    positive_positions = np.where(
        classes == 1
    )[0]

    if positive_positions.size == 0:
        return np.zeros(
            len(features),
            dtype=float,
        )

    return np.asarray(
        probabilities[
            :,
            int(
                positive_positions[0]
            ),
        ],
        dtype=float,
    )


def train_investment_model(
    model: Any,
    *,
    train_frame: pd.DataFrame,
    evaluation_frame: pd.DataFrame,
    feature_columns: list[str],
    target_column: str,
) -> InvestmentTrainingResult:
    """Fit and evaluate an investment classifier."""

    _validate_columns(
        train_frame,
        feature_columns=feature_columns,
        target_column=target_column,
    )

    _validate_columns(
        evaluation_frame,
        feature_columns=feature_columns,
        target_column=target_column,
    )

    train = train_frame.dropna(
        subset=[
            target_column,
        ]
    ).copy()

    evaluation = evaluation_frame.dropna(
        subset=[
            target_column,
        ]
    ).copy()

    if train.empty:
        raise ValueError(
            "Training frame is empty after target filtering."
        )

    if evaluation.empty:
        raise ValueError(
            "Evaluation frame is empty after target filtering."
        )

    x_train = train[
        feature_columns
    ]

    y_train = (
        train[target_column]
        .astype(int)
    )

    x_evaluation = evaluation[
        feature_columns
    ]

    y_evaluation = (
        evaluation[target_column]
        .astype(int)
    )

    model.fit(
        x_train,
        y_train,
    )

    predictions = np.asarray(
        model.predict(
            x_evaluation
        ),
        dtype=int,
    )

    probabilities = (
        _positive_class_probability(
            model,
            x_evaluation,
        )
    )

    metrics = (
        calculate_classification_metrics(
            y_evaluation.to_numpy(),
            predictions,
            probabilities,
        )
    )

    return InvestmentTrainingResult(
        model=model,
        metrics=metrics,
        predictions=predictions,
        probabilities=probabilities,
    )