"""Build leakage-safe forecasting datasets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import pandas as pd


@dataclass(frozen=True)
class ForecastingDatasetResult:
    """Result of a forecasting dataset build."""

    dataset: pd.DataFrame
    horizon_months: int
    target_column: str
    feature_columns: list[str]
    row_count: int


def _validate_required_columns(
    frame: pd.DataFrame,
    required_columns: Sequence[str],
) -> None:
    missing_columns = [
        column
        for column in required_columns
        if column not in frame.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing forecasting columns: "
            f"{missing_columns}"
        )


def build_forecasting_dataset(
    frame: pd.DataFrame,
    *,
    entity_column: str,
    timestamp_column: str,
    value_column: str,
    feature_columns: Sequence[str],
    horizon_months: int,
) -> ForecastingDatasetResult:
    """Build a forward-looking forecasting dataset."""

    if horizon_months <= 0:
        raise ValueError(
            "horizon_months must be positive."
        )

    resolved_feature_columns = list(
        feature_columns
    )

    required_columns = [
        entity_column,
        timestamp_column,
        value_column,
        *resolved_feature_columns,
    ]

    _validate_required_columns(
        frame,
        required_columns,
    )

    working = frame[
        list(
            dict.fromkeys(
                required_columns
            )
        )
    ].copy()

    working[
        timestamp_column
    ] = pd.to_datetime(
        working[
            timestamp_column
        ],
        errors="coerce",
    )

    working = working.dropna(
        subset=[
            entity_column,
            timestamp_column,
            value_column,
        ]
    )

    working = working.sort_values(
        [
            entity_column,
            timestamp_column,
        ]
    ).reset_index(
        drop=True
    )

    target_column = (
        f"future_{value_column}_"
        f"{horizon_months}m"
    )

    working[
        target_column
    ] = (
        working.groupby(
            entity_column,
            sort=False,
        )[
            value_column
        ]
        .shift(
            -horizon_months
        )
    )

    output_columns = list(
        dict.fromkeys(
            [
                entity_column,
                timestamp_column,
                value_column,
                *resolved_feature_columns,
                target_column,
            ]
        )
    )

    dataset = (
        working[
            output_columns
        ]
        .dropna(
            subset=[
                *resolved_feature_columns,
                target_column,
            ]
        )
        .reset_index(
            drop=True
        )
    )

    return ForecastingDatasetResult(
        dataset=dataset,
        horizon_months=horizon_months,
        target_column=target_column,
        feature_columns=resolved_feature_columns,
        row_count=len(
            dataset
        ),
    )