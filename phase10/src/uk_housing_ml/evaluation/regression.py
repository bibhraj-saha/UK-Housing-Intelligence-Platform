"""Regression evaluation metrics."""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


def calculate_regression_metrics(
    y_true: Any,
    y_pred: Any,
) -> dict[str, float]:
    """Calculate standard regression metrics."""

    true_values = np.asarray(
        y_true,
        dtype=float,
    )

    predicted_values = np.asarray(
        y_pred,
        dtype=float,
    )

    if true_values.shape != predicted_values.shape:
        raise ValueError(
            "y_true and y_pred must have "
            "the same shape."
        )

    if true_values.size == 0:
        raise ValueError(
            "Cannot evaluate empty arrays."
        )

    valid_mask = (
        np.isfinite(true_values)
        & np.isfinite(predicted_values)
    )

    if not valid_mask.any():
        raise ValueError(
            "No finite prediction pairs "
            "were available."
        )

    true_values = true_values[
        valid_mask
    ]

    predicted_values = predicted_values[
        valid_mask
    ]

    mae = mean_absolute_error(
        true_values,
        predicted_values,
    )

    rmse = np.sqrt(
        mean_squared_error(
            true_values,
            predicted_values,
        )
    )

    if len(true_values) < 2:
        r2 = float("nan")
    else:
        r2 = r2_score(
            true_values,
            predicted_values,
        )

    return {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "evaluated_rows": int(
            len(true_values)
        ),
    }