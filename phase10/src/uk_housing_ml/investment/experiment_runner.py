"""Experiment orchestration for investment prediction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from uk_housing_ml.investment.model_factory import (
    build_investment_model,
)
from uk_housing_ml.investment.trainer import (
    train_investment_model,
)


@dataclass(frozen=True)
class InvestmentExperimentResult:
    """Result from model comparison and final testing."""

    best_model_name: str
    best_model: Any
    validation_results: dict[str, dict[str, Any]]
    test_metrics: dict[str, float | int | None]
    test_predictions: pd.DataFrame


def _selection_value(
    metrics: dict[str, float | int | None],
    *,
    metric_name: str,
) -> float:
    value = metrics.get(
        metric_name
    )

    if value is None:
        return float("-inf")

    return float(value)


def run_investment_experiment(
    *,
    train_frame: pd.DataFrame,
    validation_frame: pd.DataFrame,
    test_frame: pd.DataFrame,
    feature_columns: list[str],
    target_column: str,
    model_configs: dict[str, dict[str, Any]],
    selection_metric: str = "roc_auc",
    random_state: int = 42,
    identifier_columns: list[str] | None = None,
) -> InvestmentExperimentResult:
    """Compare models on validation data and test the winner."""

    if not model_configs:
        raise ValueError(
            "At least one investment model is required."
        )

    validation_results: dict[
        str,
        dict[str, Any],
    ] = {}

    best_model_name: str | None = None
    best_metric_value = float("-inf")

    for model_name, model_config in (
        model_configs.items()
    ):
        model = build_investment_model(
            model_name,
            random_state=random_state,
            model_parameters=model_config.get(
                "parameters",
                {},
            ),
        )

        result = train_investment_model(
            model,
            train_frame=train_frame,
            evaluation_frame=validation_frame,
            feature_columns=feature_columns,
            target_column=target_column,
        )

        validation_results[model_name] = {
            "metrics": result.metrics,
        }

        metric_value = _selection_value(
            result.metrics,
            metric_name=selection_metric,
        )

        if metric_value > best_metric_value:
            best_metric_value = metric_value
            best_model_name = model_name

    if best_model_name is None:
        raise RuntimeError(
            "No investment model could be selected."
        )

    combined_training = pd.concat(
        [
            train_frame,
            validation_frame,
        ],
        ignore_index=True,
    )

    best_config = model_configs[
        best_model_name
    ]

    final_model = build_investment_model(
        best_model_name,
        random_state=random_state,
        model_parameters=best_config.get(
            "parameters",
            {},
        ),
    )

    final_result = train_investment_model(
        final_model,
        train_frame=combined_training,
        evaluation_frame=test_frame,
        feature_columns=feature_columns,
        target_column=target_column,
    )

    valid_test = test_frame.dropna(
        subset=[
            target_column,
        ]
    ).copy()

    prediction_frame = pd.DataFrame(
        index=valid_test.index
    )

    for column in (
        identifier_columns
        if identifier_columns is not None
        else []
    ):
        if column in valid_test.columns:
            prediction_frame[column] = (
                valid_test[column]
            )

    prediction_frame["actual"] = (
        valid_test[target_column]
        .astype(int)
    )

    prediction_frame["prediction"] = (
        final_result.predictions
    )

    prediction_frame[
        "opportunity_probability"
    ] = final_result.probabilities

    prediction_frame["model_name"] = (
        best_model_name
    )

    prediction_frame = (
        prediction_frame
        .reset_index(drop=True)
    )

    return InvestmentExperimentResult(
        best_model_name=best_model_name,
        best_model=final_result.model,
        validation_results=validation_results,
        test_metrics=final_result.metrics,
        test_predictions=prediction_frame,
    )