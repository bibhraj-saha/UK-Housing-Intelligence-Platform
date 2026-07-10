"""Run forecasting model experiments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

import pandas as pd

from uk_housing_ml.forecasting.trainer import (
    ForecastModelResult,
    train_forecasting_model,
)


@dataclass(frozen=True)
class ForecastExperimentResult:
    """Forecasting experiment result."""

    best_model_name: str
    best_model: Any
    validation_results: dict[
        str,
        dict[str, Any],
    ]
    test_metrics: dict[
        str,
        float | int,
    ]
    test_predictions: pd.DataFrame


def _build_prediction_frame(
    *,
    frame: pd.DataFrame,
    entity_column: str,
    timestamp_column: str,
    target_column: str,
    predictions: pd.Series,
    model_name: str,
    horizon_months: int,
) -> pd.DataFrame:
    output = frame[
        [
            entity_column,
            timestamp_column,
        ]
    ].copy()

    output[
        "actual"
    ] = frame[
        target_column
    ].to_numpy()

    output[
        "prediction"
    ] = predictions.to_numpy()

    output[
        "residual"
    ] = (
        output[
            "actual"
        ]
        - output[
            "prediction"
        ]
    )

    output[
        "absolute_error"
    ] = output[
        "residual"
    ].abs()

    output[
        "model_name"
    ] = model_name

    output[
        "horizon_months"
    ] = horizon_months

    return output.reset_index(
        drop=True
    )


def run_forecasting_experiment(
    *,
    train_frame: pd.DataFrame,
    validation_frame: pd.DataFrame,
    test_frame: pd.DataFrame,
    feature_columns: Sequence[str],
    target_column: str,
    entity_column: str,
    timestamp_column: str,
    horizon_months: int,
    models: dict[str, dict[str, Any]],
    selection_metric: str = "rmse",
    random_state: int = 42,
    naive_feature_column: str = (
        "price_lag_1m"
    ),
) -> ForecastExperimentResult:
    """Run validation selection and final test evaluation."""

    validation_results: dict[
        str,
        dict[str, Any],
    ] = {}

    trained_validation_results: dict[
        str,
        ForecastModelResult,
    ] = {}

    for model_name, model_config in (
        models.items()
    ):
        if not bool(
            model_config.get(
                "enabled",
                True,
            )
        ):
            continue

        result = train_forecasting_model(
            model_name=model_name,
            train_frame=train_frame,
            evaluation_frame=validation_frame,
            feature_columns=feature_columns,
            target_column=target_column,
            random_state=random_state,
            naive_feature_column=(
                naive_feature_column
            ),
            model_parameters=(
                model_config.get(
                    "parameters",
                    {},
                )
            ),
        )

        trained_validation_results[
            model_name
        ] = result

        validation_results[
            model_name
        ] = {
            "metrics": result.metrics,
        }

    if not trained_validation_results:
        raise ValueError(
            "No forecasting models were enabled."
        )

    if selection_metric not in {
        "mae",
        "rmse",
        "mape",
    }:
        raise ValueError(
            "Unsupported forecasting "
            "selection metric: "
            f"{selection_metric}"
        )

    best_model_name = min(
        trained_validation_results,
        key=lambda name: float(
            trained_validation_results[
                name
            ].metrics[
                selection_metric
            ]
        ),
    )

    combined_train = pd.concat(
        [
            train_frame,
            validation_frame,
        ],
        ignore_index=True,
    )

    best_config = models[
        best_model_name
    ]

    final_result = train_forecasting_model(
        model_name=best_model_name,
        train_frame=combined_train,
        evaluation_frame=test_frame,
        feature_columns=feature_columns,
        target_column=target_column,
        random_state=random_state,
        naive_feature_column=(
            naive_feature_column
        ),
        model_parameters=(
            best_config.get(
                "parameters",
                {},
            )
        ),
    )

    prediction_frame = (
        _build_prediction_frame(
            frame=test_frame,
            entity_column=entity_column,
            timestamp_column=timestamp_column,
            target_column=target_column,
            predictions=(
                final_result.predictions
            ),
            model_name=best_model_name,
            horizon_months=(
                horizon_months
            ),
        )
    )

    return ForecastExperimentResult(
        best_model_name=best_model_name,
        best_model=final_result.model,
        validation_results=(
            validation_results
        ),
        test_metrics=(
            final_result.metrics
        ),
        test_predictions=(
            prediction_frame
        ),
    )