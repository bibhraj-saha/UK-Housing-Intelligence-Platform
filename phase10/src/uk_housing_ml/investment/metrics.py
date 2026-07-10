"""Classification metrics for investment prediction."""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def calculate_classification_metrics(
    y_true: Any,
    y_pred: Any,
    y_probability: Any | None = None,
) -> dict[str, float | int | None]:
    """Calculate binary classification metrics."""

    true_values = np.asarray(
        y_true
    )

    predicted_values = np.asarray(
        y_pred
    )

    if true_values.shape != predicted_values.shape:
        raise ValueError(
            "Metric input shapes must match."
        )

    if true_values.size == 0:
        raise ValueError(
            "Metric inputs cannot be empty."
        )

    roc_auc: float | None = None

    if y_probability is not None:
        probabilities = np.asarray(
            y_probability
        )

        if probabilities.shape != true_values.shape:
            raise ValueError(
                "Probability input shape must match targets."
            )

        if np.unique(
            true_values
        ).size == 2:
            roc_auc = float(
                roc_auc_score(
                    true_values,
                    probabilities,
                )
            )

    return {
        "accuracy": float(
            accuracy_score(
                true_values,
                predicted_values,
            )
        ),
        "precision": float(
            precision_score(
                true_values,
                predicted_values,
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                true_values,
                predicted_values,
                zero_division=0,
            )
        ),
        "f1": float(
            f1_score(
                true_values,
                predicted_values,
                zero_division=0,
            )
        ),
        "roc_auc": roc_auc,
        "evaluated_rows": int(
            true_values.size
        ),
    }