"""Train Phase 10 housing forecasting models."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import yaml


PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

PHASE10_ROOT = (
    PROJECT_ROOT
    / "phase10"
)

SRC_ROOT = (
    PHASE10_ROOT
    / "src"
)

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(SRC_ROOT),
    )


from uk_housing_ml.forecasting.experiment_runner import (  # noqa: E402
    run_forecasting_experiment,
)


def _load_yaml(
    path: Path,
) -> dict[str, Any]:
    with path.open(
        "r",
        encoding="utf-8",
    ) as handle:
        loaded = yaml.safe_load(
            handle
        )

    if not isinstance(
        loaded,
        dict,
    ):
        raise ValueError(
            f"Configuration must be a mapping: {path}"
        )

    return loaded


def _resolve_project_path(
    value: str,
) -> Path:
    return (
        PROJECT_ROOT
        / value
    ).resolve()


def main() -> int:
    config_path = (
        PHASE10_ROOT
        / "config"
        / "forecasting"
        / "housing_market_forecasting.yaml"
    )

    config = _load_yaml(
        config_path
    )

    columns_config = config[
        "columns"
    ]

    output_config = config[
        "output"
    ]

    entity_column = columns_config[
        "entity"
    ]

    timestamp_column = columns_config[
        "timestamp"
    ]

    value_column = columns_config[
        "value"
    ]

    feature_columns = list(
        config[
            "features"
        ]
    )

    dataset_directory = (
        _resolve_project_path(
            output_config[
                "dataset_directory"
            ]
        )
    )

    model_directory = (
        _resolve_project_path(
            output_config[
                "model_directory"
            ]
        )
    )

    prediction_directory = (
        _resolve_project_path(
            output_config[
                "prediction_directory"
            ]
        )
    )

    report_directory = (
        _resolve_project_path(
            output_config[
                "report_directory"
            ]
        )
    )

    for directory in [
        model_directory,
        prediction_directory,
        report_directory,
    ]:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    dataset_manifest_path = (
        dataset_directory
        / "forecasting_dataset_manifest.json"
    )

    dataset_manifest = json.loads(
        dataset_manifest_path.read_text(
            encoding="utf-8"
        )
    )

    generated_at = (
        datetime.now(
            timezone.utc
        ).isoformat()
    )

    overall_report: dict[str, Any] = {
        "task_name": config[
            "task_name"
        ],
        "generated_at_utc": generated_at,
        "selection_metric": config[
            "selection"
        ][
            "metric"
        ],
        "horizons": {},
    }

    print("=" * 72)
    print(
        "PHASE 10 HOUSING MARKET FORECASTING"
    )
    print("=" * 72)

    for horizon_months in config[
        "horizons"
    ]:
        horizon_months = int(
            horizon_months
        )

        horizon_key = str(
            horizon_months
        )

        dataset_info = (
            dataset_manifest[
                "horizons"
            ].get(
                horizon_key,
                {},
            )
        )

        if (
            dataset_info.get(
                "status"
            )
            != "dataset_built"
        ):
            overall_report[
                "horizons"
            ][
                horizon_key
            ] = {
                "status": "not_trained",
                "reason": dataset_info.get(
                    "reason",
                    "Forecasting dataset unavailable.",
                ),
            }

            print("-" * 72)
            print(
                f"Horizon: {horizon_months} months"
            )
            print(
                "Status: not_trained"
            )

            continue

        horizon_dataset_directory = (
            dataset_directory
            / f"{horizon_months}_months"
        )

        train_frame = pd.read_parquet(
            horizon_dataset_directory
            / "train.parquet"
        )

        validation_frame = pd.read_parquet(
            horizon_dataset_directory
            / "validation.parquet"
        )

        test_frame = pd.read_parquet(
            horizon_dataset_directory
            / "test.parquet"
        )

        target_column = (
            f"future_{value_column}_"
            f"{horizon_months}m"
        )

        result = run_forecasting_experiment(
            train_frame=train_frame,
            validation_frame=validation_frame,
            test_frame=test_frame,
            feature_columns=feature_columns,
            target_column=target_column,
            entity_column=entity_column,
            timestamp_column=timestamp_column,
            horizon_months=horizon_months,
            models=config[
                "models"
            ],
            selection_metric=config[
                "selection"
            ][
                "metric"
            ],
            random_state=int(
                config[
                    "runtime"
                ][
                    "random_state"
                ]
            ),
            naive_feature_column=(
                "price_lag_1m"
            ),
        )

        horizon_model_directory = (
            model_directory
            / f"{horizon_months}_months"
        )

        horizon_prediction_directory = (
            prediction_directory
            / f"{horizon_months}_months"
        )

        horizon_model_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        horizon_prediction_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        model_path = (
            horizon_model_directory
            / "best_model.joblib"
        )

        prediction_path = (
            horizon_prediction_directory
            / "test_predictions.parquet"
        )

        joblib.dump(
            result.best_model,
            model_path,
        )

        result.test_predictions.to_parquet(
            prediction_path,
            index=False,
        )

        horizon_report = {
            "status": "trained",
            "horizon_months": (
                horizon_months
            ),
            "target_column": (
                target_column
            ),
            "feature_columns": (
                feature_columns
            ),
            "best_model_name": (
                result.best_model_name
            ),
            "validation_results": (
                result.validation_results
            ),
            "test_metrics": (
                result.test_metrics
            ),
            "row_counts": {
                "train": int(
                    len(
                        train_frame
                    )
                ),
                "validation": int(
                    len(
                        validation_frame
                    )
                ),
                "test": int(
                    len(
                        test_frame
                    )
                ),
            },
            "model_path": str(
                model_path.relative_to(
                    PROJECT_ROOT
                )
            ),
            "prediction_path": str(
                prediction_path.relative_to(
                    PROJECT_ROOT
                )
            ),
        }

        overall_report[
            "horizons"
        ][
            horizon_key
        ] = horizon_report

        model_manifest_path = (
            horizon_model_directory
            / "model_manifest.json"
        )

        model_manifest_path.write_text(
            json.dumps(
                {
                    "task_name": config[
                        "task_name"
                    ],
                    "generated_at_utc": (
                        generated_at
                    ),
                    **horizon_report,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        print("-" * 72)
        print(
            f"Horizon: {horizon_months} months"
        )
        print(
            "Status: trained"
        )
        print(
            "Best model:",
            result.best_model_name,
        )

        print(
            "Test MAE:",
            f"{result.test_metrics['mae']:.6f}",
        )

        print(
            "Test RMSE:",
            f"{result.test_metrics['rmse']:.6f}",
        )

        print(
            "Test R2:",
            f"{result.test_metrics['r2']:.6f}",
        )

        print(
            "Test MAPE:",
            f"{result.test_metrics['mape']:.6f}",
        )

    report_path = (
        report_directory
        / "forecasting_evaluation_report.json"
    )

    report_path.write_text(
        json.dumps(
            overall_report,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("-" * 72)
    print(
        "Report:",
        report_path,
    )
    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )