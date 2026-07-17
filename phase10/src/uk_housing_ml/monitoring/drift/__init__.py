"""Feature drift calculations."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd


def calculate_numeric_drift(
    *,
    reference: pd.Series,
    current: pd.Series,
    threshold: float = 0.25,
) -> dict[str, float | bool | None]:
    """Calculate standardized mean-shift drift."""

    if threshold < 0:
        raise ValueError(
            "threshold must be non-negative."
        )

    reference_values = pd.to_numeric(
        reference,
        errors="coerce",
    ).dropna()

    current_values = pd.to_numeric(
        current,
        errors="coerce",
    ).dropna()

    if (
        reference_values.empty
        or current_values.empty
    ):
        return {
            "reference_mean": None,
            "current_mean": None,
            "reference_std": None,
            "standardized_mean_shift": None,
            "drift_detected": False,
        }

    reference_mean = float(
        reference_values.mean()
    )

    current_mean = float(
        current_values.mean()
    )

    reference_std = float(
        reference_values.std(
            ddof=0
        )
    )

    if (
        not math.isfinite(
            reference_std
        )
        or np.isclose(
            reference_std,
            0.0,
        )
    ):
        shift = (
            0.0
            if np.isclose(
                reference_mean,
                current_mean,
            )
            else float("inf")
        )
    else:
        shift = abs(
            current_mean
            - reference_mean
        ) / reference_std

    return {
        "reference_mean": reference_mean,
        "current_mean": current_mean,
        "reference_std": reference_std,
        "standardized_mean_shift": float(
            shift
        ),
        "drift_detected": bool(
            shift > threshold
        ),
    }