"""Forecasting evaluation metrics."""

from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


def calculate_forecasting_metrics(
    actual: object,
    prediction: object,
) -> dict[str, float | int]:
    """Calculate regression metrics for forecasts."""

    actual_array = np.asarray(
        actual,
        dtype=float,
    )

    prediction_array = np.asarray(
        prediction,
        dtype=float,
    )

    if actual_array.shape != prediction_array.shape:
        raise ValueError(
            "Actual and prediction shapes must match."
        )

    if actual_array.size == 0:
        raise ValueError(
            "Forecasting metrics require "
            "at least one observation."
        )

    mae = mean_absolute_error(
        actual_array,
        prediction_array,
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual_array,
            prediction_array,
        )
    )

    r2 = r2_score(
        actual_array,
        prediction_array,
    )

    non_zero_mask = (
        np.abs(
            actual_array
        )
        > 1e-12
    )

    if non_zero_mask.any():
        mape = np.mean(
            np.abs(
                (
                    actual_array[
                        non_zero_mask
                    ]
                    - prediction_array[
                        non_zero_mask
                    ]
                )
                / actual_array[
                    non_zero_mask
                ]
            )
        ) * 100.0
    else:
        mape = float(
            "nan"
        )

    return {
        "mae": float(
            mae
        ),
        "rmse": float(
            rmse
        ),
        "r2": float(
            r2
        ),
        "mape": float(
            mape
        ),
        "evaluated_rows": int(
            actual_array.size
        ),
    }