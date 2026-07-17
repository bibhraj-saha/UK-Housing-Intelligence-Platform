"""Build dashboard-ready ML serving datasets."""

from __future__ import annotations

import pandas as pd


def _latest_prediction_per_entity(
    *,
    frame: pd.DataFrame,
    entity_column: str,
) -> pd.DataFrame:
    if entity_column not in frame.columns:
        raise ValueError(
            "Prediction frame is missing "
            f"entity column '{entity_column}'."
        )

    result = frame.copy()

    temporal_candidates = [
        column
        for column in [
            "period_end",
            "timestamp",
        ]
        if column in result.columns
    ]

    if temporal_candidates:
        temporal_column = (
            temporal_candidates[0]
        )

        result[
            temporal_column
        ] = pd.to_datetime(
            result[
                temporal_column
            ],
            errors="coerce",
        )

        result = (
            result.sort_values(
                [
                    entity_column,
                    temporal_column,
                ]
            )
            .groupby(
                entity_column,
                as_index=False,
            )
            .tail(
                1
            )
        )
    else:
        result = (
            result.groupby(
                entity_column,
                as_index=False,
            )
            .tail(
                1
            )
        )

    return result


def build_area_ml_serving_dataset(
    *,
    recommendations: pd.DataFrame,
    investment_predictions: pd.DataFrame,
    price_predictions: pd.DataFrame,
    growth_predictions: pd.DataFrame,
    entity_column: str = "lsoa_code",
) -> pd.DataFrame:
    """Combine Phase 10 outputs by area."""

    if entity_column not in (
        recommendations.columns
    ):
        raise ValueError(
            "Recommendations are missing "
            f"'{entity_column}'."
        )

    serving = (
        recommendations.copy()
    )

    investment = (
        _latest_prediction_per_entity(
            frame=investment_predictions,
            entity_column=entity_column,
        )
    )

    price = (
        _latest_prediction_per_entity(
            frame=price_predictions,
            entity_column=entity_column,
        )
    )

    growth = (
        _latest_prediction_per_entity(
            frame=growth_predictions,
            entity_column=entity_column,
        )
    )

    investment_columns = [
        entity_column,
        "opportunity_probability",
    ]

    price = price.rename(
        columns={
            "prediction": (
                "predicted_future_price"
            ),
        }
    )

    growth = growth.rename(
        columns={
            "prediction": (
                "predicted_future_growth"
            ),
        }
    )

    serving = serving.merge(
        investment[
            investment_columns
        ],
        on=entity_column,
        how="left",
    )

    serving = serving.merge(
        price[
            [
                entity_column,
                "predicted_future_price",
            ]
        ],
        on=entity_column,
        how="left",
    )

    serving = serving.merge(
        growth[
            [
                entity_column,
                "predicted_future_growth",
            ]
        ],
        on=entity_column,
        how="left",
    )

    return serving.sort_values(
        "recommendation_rank"
    ).reset_index(
        drop=True
    )