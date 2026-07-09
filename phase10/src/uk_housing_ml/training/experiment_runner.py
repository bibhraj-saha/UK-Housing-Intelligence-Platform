"""Run reproducible regression experiments."""

from __future__ import annotations

import json
from datetime import (
    datetime,
    timezone,
)
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import yaml

from uk_housing_ml.evaluation.regression import (
    calculate_regression_metrics,
)
from uk_housing_ml.models.factory import (
    build_model,
)
from uk_housing_ml.training.dataset_loader import (
    load_training_splits,
)
from uk_housing_ml.training.model_trainer import (
    train_model,
)


def _load_yaml(
    config_path: Path,
) -> dict[str, Any]:
    with Path(config_path).open(
        "r",
        encoding="utf-8",
    ) as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError(
            "Model configuration must "
            "be a mapping."
        )

    return config


def _validate_columns(
    splits: dict[str, pd.DataFrame],
    feature_columns: list[str],
    target_column: str,
) -> None:
    required_columns = set(
        feature_columns
        + [
            target_column,
        ]
    )

    for split_name, frame in splits.items():
        missing_columns = sorted(
            required_columns
            - set(frame.columns)
        )

        if missing_columns:
            raise ValueError(
                f"{split_name} split is missing "
                f"columns: {missing_columns}"
            )


def _build_prediction_frame(
    source_frame: pd.DataFrame,
    predictions: Any,
    target_column: str,
    model_name: str,
    identifier_columns: list[str],
) -> pd.DataFrame:
    available_identifiers = [
        column
        for column in identifier_columns
        if column in source_frame.columns
    ]

    result = source_frame[
        available_identifiers
    ].copy()

    result["actual"] = source_frame[
        target_column
    ].to_numpy()

    result["prediction"] = predictions

    result["residual"] = (
        result["actual"]
        - result["prediction"]
    )

    result["absolute_error"] = (
        result["residual"].abs()
    )

    result["model_name"] = model_name

    return result


def run_regression_experiment(
    project_root: Path,
    config_path: Path,
) -> dict[str, Any]:
    """Train, select and test regression models."""

    project_root = Path(
        project_root
    ).resolve()

    config_path = Path(
        config_path
    ).resolve()

    config = _load_yaml(
        config_path
    )

    task_name = str(
        config["task_name"]
    )

    target_column = str(
        config["target_column"]
    )

    feature_columns = [
        str(column)
        for column in config[
            "feature_columns"
        ]
    ]

    identifier_columns = [
        str(column)
        for column in config.get(
            "identifier_columns",
            [],
        )
    ]

    dataset_directory = (
        project_root
        / config["dataset_directory"]
    )

    splits = load_training_splits(
        dataset_directory=(
            dataset_directory
        )
    )

    _validate_columns(
        splits=splits,
        feature_columns=feature_columns,
        target_column=target_column,
    )

    validation_results: dict[
        str,
        dict[str, Any],
    ] = {}

    fitted_models: dict[
        str,
        Any,
    ] = {}

    model_definitions = config[
        "models"
    ]

    for model_name, model_config in (
        model_definitions.items()
    ):
        if not bool(
            model_config.get(
                "enabled",
                True,
            )
        ):
            continue

        model = build_model(
            model_name=model_name,
            model_config=model_config,
        )

        fitted_model, metrics = train_model(
            model=model,
            train_frame=splits["train"],
            evaluation_frame=(
                splits["validation"]
            ),
            feature_columns=feature_columns,
            target_column=target_column,
        )

        fitted_models[
            model_name
        ] = fitted_model

        validation_results[
            model_name
        ] = {
            "metrics": metrics,
        }

    if not validation_results:
        raise ValueError(
            "No enabled models were found."
        )

    best_model_name = min(
        validation_results,
        key=lambda name: (
            validation_results[
                name
            ]["metrics"]["rmse"]
        ),
    )

    best_model = fitted_models[
        best_model_name
    ]

    test_predictions = best_model.predict(
        splits["test"][
            feature_columns
        ]
    )

    test_metrics = (
        calculate_regression_metrics(
            y_true=splits["test"][
                target_column
            ],
            y_pred=test_predictions,
        )
    )

    artifact_directory = (
        project_root
        / config["artifact_directory"]
    )

    report_directory = (
        project_root
        / config["report_directory"]
    )

    prediction_directory = (
        project_root
        / config["prediction_directory"]
    )

    for directory in (
        artifact_directory,
        report_directory,
        prediction_directory,
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    model_path = (
        artifact_directory
        / "best_model.joblib"
    )

    joblib.dump(
        best_model,
        model_path,
    )

    prediction_frame = (
        _build_prediction_frame(
            source_frame=splits["test"],
            predictions=test_predictions,
            target_column=target_column,
            model_name=best_model_name,
            identifier_columns=(
                identifier_columns
            ),
        )
    )

    prediction_path = (
        prediction_directory
        / "test_predictions.parquet"
    )

    prediction_frame.to_parquet(
        prediction_path,
        index=False,
    )

    generated_at = (
        datetime.now(
            timezone.utc
        ).isoformat()
    )

    report = {
        "task_name": task_name,
        "generated_at_utc": generated_at,
        "selection_metric": (
            "validation_rmse"
        ),
        "target_column": target_column,
        "feature_columns": (
            feature_columns
        ),
        "best_model_name": (
            best_model_name
        ),
        "validation_results": (
            validation_results
        ),
        "test_metrics": test_metrics,
        "row_counts": {
            split_name: int(
                len(frame)
            )
            for split_name, frame
            in splits.items()
        },
        "model_path": str(
            model_path.relative_to(
                project_root
            )
        ),
        "prediction_path": str(
            prediction_path.relative_to(
                project_root
            )
        ),
    }

    report_path = (
        report_directory
        / "evaluation_report.json"
    )

    report_path.write_text(
        json.dumps(
            report,
            indent=2,
            allow_nan=False,
        ),
        encoding="utf-8",
    )

    manifest = {
        "task_name": task_name,
        "generated_at_utc": generated_at,
        "model_name": best_model_name,
        "target_column": target_column,
        "feature_columns": (
            feature_columns
        ),
        "selection_metric": (
            "validation_rmse"
        ),
        "validation_metrics": (
            validation_results[
                best_model_name
            ]["metrics"]
        ),
        "test_metrics": test_metrics,
        "artifact": str(
            model_path.relative_to(
                project_root
            )
        ),
    }

    manifest_path = (
        artifact_directory
        / "model_manifest.json"
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            allow_nan=False,
        ),
        encoding="utf-8",
    )

    return report