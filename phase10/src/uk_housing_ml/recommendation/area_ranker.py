"""Configurable area-ranking logic for Phase 10."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class AreaRecommendationResult:
    """Result returned by the area recommendation workflow."""

    recommendations: pd.DataFrame
    feature_columns: list[str]
    weights: dict[str, float]


def _validate_weights(
    weights: dict[str, float],
) -> None:
    if not weights:
        raise ValueError(
            "At least one recommendation weight is required."
        )

    if any(
        float(weight) < 0.0
        for weight in weights.values()
    ):
        raise ValueError(
            "Recommendation weights cannot be negative."
        )

    total = sum(
        float(weight)
        for weight in weights.values()
    )

    if not np.isclose(
        total,
        1.0,
    ):
        raise ValueError(
            "Recommendation weights must sum to 1.0."
        )


def _percentile_score(
    series: pd.Series,
    *,
    higher_is_better: bool,
) -> pd.Series:
    numeric = pd.to_numeric(
        series,
        errors="coerce",
    )

    ranked = numeric.rank(
        method="average",
        pct=True,
    )

    if not higher_is_better:
        ranked = 1.0 - ranked

    return (
        ranked
        .fillna(0.0)
        .clip(
            lower=0.0,
            upper=1.0,
        )
    )


def _latest_entity_snapshot(
    frame: pd.DataFrame,
    *,
    entity_column: str,
    timestamp_column: str,
) -> pd.DataFrame:
    required = {
        entity_column,
        timestamp_column,
    }

    missing = sorted(
        required.difference(
            frame.columns
        )
    )

    if missing:
        raise ValueError(
            "Missing required snapshot columns: "
            f"{missing}"
        )

    working = frame.copy()

    working[timestamp_column] = pd.to_datetime(
        working[timestamp_column],
        errors="coerce",
    )

    working = working.dropna(
        subset=[
            entity_column,
            timestamp_column,
        ]
    )

    if working.empty:
        raise ValueError(
            "No valid entity-timestamp rows are available."
        )

    working = working.sort_values(
        by=[
            entity_column,
            timestamp_column,
        ]
    )

    return (
        working
        .groupby(
            entity_column,
            as_index=False,
        )
        .tail(1)
        .reset_index(drop=True)
    )


def build_area_recommendations(
    frame: pd.DataFrame,
    *,
    config: dict[str, Any],
) -> AreaRecommendationResult:
    """Build ranked area recommendations from latest features."""

    entity_column = str(
        config.get(
            "entity_column",
            "lsoa_code",
        )
    )

    timestamp_column = str(
        config.get(
            "timestamp_column",
            "timestamp",
        )
    )

    feature_config = config.get(
        "features",
        {},
    )

    if not isinstance(
        feature_config,
        dict,
    ) or not feature_config:
        raise ValueError(
            "Recommendation feature configuration is required."
        )

    weights = {
        str(feature_name): float(
            definition["weight"]
        )
        for feature_name, definition in (
            feature_config.items()
        )
    }

    _validate_weights(
        weights
    )

    feature_columns = list(
        feature_config.keys()
    )

    required_columns = {
        entity_column,
        timestamp_column,
        *feature_columns,
    }

    missing_columns = sorted(
        required_columns.difference(
            frame.columns
        )
    )

    if missing_columns:
        raise ValueError(
            "Missing recommendation columns: "
            f"{missing_columns}"
        )

    latest = _latest_entity_snapshot(
        frame,
        entity_column=entity_column,
        timestamp_column=timestamp_column,
    )

    output = latest[
        [
            entity_column,
            timestamp_column,
            *feature_columns,
        ]
    ].copy()

    component_columns: list[str] = []

    for feature_name, definition in (
        feature_config.items()
    ):
        higher_is_better = bool(
            definition.get(
                "higher_is_better",
                True,
            )
        )

        component_column = (
            f"{feature_name}_component_score"
        )

        output[component_column] = (
            _percentile_score(
                output[feature_name],
                higher_is_better=higher_is_better,
            )
        )

        component_columns.append(
            component_column
        )

    output["recommendation_score"] = 0.0

    for feature_name, weight in weights.items():
        component_column = (
            f"{feature_name}_component_score"
        )

        output["recommendation_score"] += (
            output[component_column]
            * weight
        )

    output["recommendation_score"] = (
        output["recommendation_score"]
        .clip(
            lower=0.0,
            upper=1.0,
        )
    )

    output = output.sort_values(
        by=[
            "recommendation_score",
            entity_column,
        ],
        ascending=[
            False,
            True,
        ],
    ).reset_index(drop=True)

    output["recommendation_rank"] = (
        np.arange(
            1,
            len(output) + 1,
        )
    )

    output["recommendation_percentile"] = (
        1.0
        - (
            output["recommendation_rank"]
            - 1
        )
        / max(
            len(output),
            1,
        )
    )

    ordered_columns = [
        entity_column,
        timestamp_column,
        "recommendation_rank",
        "recommendation_score",
        "recommendation_percentile",
        *feature_columns,
        *component_columns,
    ]

    return AreaRecommendationResult(
        recommendations=output[
            ordered_columns
        ],
        feature_columns=feature_columns,
        weights=weights,
    )