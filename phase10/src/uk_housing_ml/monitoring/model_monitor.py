"""Model and feature monitoring reports."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from uk_housing_ml.monitoring.drift import (
    calculate_numeric_drift,
)


def build_monitoring_report(
    *,
    task_name: str,
    reference_frame: pd.DataFrame,
    current_frame: pd.DataFrame,
    feature_columns: list[str],
    drift_threshold: float,
) -> dict[str, Any]:
    """Build feature drift monitoring report."""

    missing_reference = sorted(
        set(
            feature_columns
        )
        - set(
            reference_frame.columns
        )
    )

    missing_current = sorted(
        set(
            feature_columns
        )
        - set(
            current_frame.columns
        )
    )

    if missing_reference:
        raise ValueError(
            "Missing reference features: "
            f"{missing_reference}"
        )

    if missing_current:
        raise ValueError(
            "Missing current features: "
            f"{missing_current}"
        )

    feature_results = {}

    for feature in feature_columns:
        feature_results[
            feature
        ] = calculate_numeric_drift(
            reference=reference_frame[
                feature
            ],
            current=current_frame[
                feature
            ],
            threshold=drift_threshold,
        )

    drifted_features = [
        feature
        for feature, result
        in feature_results.items()
        if bool(
            result[
                "drift_detected"
            ]
        )
    ]

    return {
        "task_name": task_name,
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "reference_rows": int(
            len(
                reference_frame
            )
        ),
        "current_rows": int(
            len(
                current_frame
            )
        ),
        "drift_threshold": (
            drift_threshold
        ),
        "monitored_feature_count": len(
            feature_columns
        ),
        "drifted_feature_count": len(
            drifted_features
        ),
        "drifted_features": (
            drifted_features
        ),
        "overall_status": (
            "drift_detected"
            if drifted_features
            else "healthy"
        ),
        "feature_results": (
            feature_results
        ),
    }