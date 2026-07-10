"""Train Phase 10 investment opportunity models."""

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

from uk_housing_ml.investment.experiment_runner import (  # noqa: E402
    run_investment_experiment,
)
from uk_housing_ml.investment.target_builder import (  # noqa: E402
    build_investment_target,
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


def _load_split(
    training_directory: Path,
    split_name: str,
) -> pd.DataFrame:
    path = (
        training_directory
        / f"{split_name}.parquet"
    )

    if not path.exists():
        raise FileNotFoundError(
            f"Training split not found: {path}"
        )

    return pd.read_parquet(
        path
    )


def _prepare_target(
    frame: pd.DataFrame,
    *,
    source_column: str,
    target_column: str,
    minimum_growth: float,
) -> pd.DataFrame:
    return build_investment_target(
        frame,
        growth_column=source_column,
        target_column=target_column,
        minimum_growth=minimum_growth,
    )


def main() -> int:
    config_path = (
        PHASE10_ROOT
        / "config"
        / "investment"
        / "investment_opportunity_prediction.yaml"
    )

    config = _load_yaml(
        config_path
    )

    paths = config[
        "paths"
    ]

    training_directory = (
        _resolve_project_path(
            paths[
                "training_directory"
            ]
        )
    )

    train_frame = _load_split(
        training_directory,
        "train",
    )

    validation_frame = _load_split(
        training_directory,
        "validation",
    )

    test_frame = _load_split(
        training_directory,
        "test",
    )

    target_config = config[
        "target"
    ]

    source_column = str(
        target_config[
            "source_column"
        ]
    )

    target_column = str(
        target_config[
            "target_column"
        ]
    )

    minimum_growth = float(
        target_config.get(
            "minimum_growth",
            0.0,
        )
    )

    train_frame = _prepare_target(
        train_frame,
        source_column=source_column,
        target_column=target_column,
        minimum_growth=minimum_growth,
    )

    validation_frame = _prepare_target(
        validation_frame,
        source_column=source_column,
        target_column=target_column,
        minimum_growth=minimum_growth,
    )

    test_frame = _prepare_target(
        test_frame,
        source_column=source_column,
        target_column=target_column,
        minimum_growth=minimum_growth,
    )

    feature_columns = [
        str(column)
        for column in config[
            "features"
        ]
    ]

    result = run_investment_experiment(
        train_frame=train_frame,
        validation_frame=validation_frame,
        test_frame=test_frame,
        feature_columns=feature_columns,
        target_column=target_column,
        model_configs=config[
            "models"
        ],
        selection_metric=str(
            config.get(
                "selection_metric",
                "roc_auc",
            )
        ),
        random_state=int(
            config.get(
                "random_state",
                42,
            )
        ),
        identifier_columns=[
            "lsoa_code",
        ],
    )

    model_path = _resolve_project_path(
        paths[
            "model_path"
        ]
    )

    manifest_path = _resolve_project_path(
        paths[
            "manifest_path"
        ]
    )

    prediction_path = _resolve_project_path(
        paths[
            "prediction_path"
        ]
    )

    report_path = _resolve_project_path(
        paths[
            "evaluation_report_path"
        ]
    )

    for path in [
        model_path,
        manifest_path,
        prediction_path,
        report_path,
    ]:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    joblib.dump(
        result.best_model,
        model_path,
    )

    result.test_predictions.to_parquet(
        prediction_path,
        index=False,
    )

    generated_at = datetime.now(
        timezone.utc
    ).isoformat()

    report = {
        "task_name": config[
            "task_name"
        ],
        "generated_at_utc": generated_at,
        "selection_metric": config[
            "selection_metric"
        ],
        "target_column": target_column,
        "target_definition": {
            "source_column": source_column,
            "minimum_growth": minimum_growth,
            "positive_class_rule": (
                f"{source_column} > "
                f"{minimum_growth}"
            ),
        },
        "feature_columns": feature_columns,
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
        "class_balance": {
            "train_positive_rate": float(
                train_frame[
                    target_column
                ].dropna().mean()
            ),
            "validation_positive_rate": float(
                validation_frame[
                    target_column
                ].dropna().mean()
            ),
            "test_positive_rate": float(
                test_frame[
                    target_column
                ].dropna().mean()
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

    report_path.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )

    best_validation_metrics = (
        result.validation_results[
            result.best_model_name
        ][
            "metrics"
        ]
    )

    manifest = {
        "task_name": config[
            "task_name"
        ],
        "generated_at_utc": generated_at,
        "model_name": (
            result.best_model_name
        ),
        "target_column": target_column,
        "feature_columns": feature_columns,
        "selection_metric": config[
            "selection_metric"
        ],
        "validation_metrics": (
            best_validation_metrics
        ),
        "test_metrics": (
            result.test_metrics
        ),
        "artifact": str(
            model_path.relative_to(
                PROJECT_ROOT
            )
        ),
    }

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("=" * 72)
    print(
        "PHASE 10 INVESTMENT OPPORTUNITY PREDICTION"
    )
    print("=" * 72)
    print(
        "Best model:",
        result.best_model_name,
    )
    print(
        "Selection metric:",
        config[
            "selection_metric"
        ],
    )
    print()
    print(
        "VALIDATION RESULTS"
    )
    print("-" * 72)

    for model_name, model_result in (
        result.validation_results.items()
    ):
        metrics = model_result[
            "metrics"
        ]

        print(
            f"{model_name}: "
            f"Accuracy="
            f"{metrics['accuracy']:.6f}, "
            f"Precision="
            f"{metrics['precision']:.6f}, "
            f"Recall="
            f"{metrics['recall']:.6f}, "
            f"F1="
            f"{metrics['f1']:.6f}, "
            f"ROC_AUC="
            f"{metrics['roc_auc']}"
        )

    print()
    print(
        "FINAL TEST RESULTS"
    )
    print("-" * 72)

    test_metrics = result.test_metrics

    print(
        f"Accuracy="
        f"{test_metrics['accuracy']:.6f}"
    )
    print(
        f"Precision="
        f"{test_metrics['precision']:.6f}"
    )
    print(
        f"Recall="
        f"{test_metrics['recall']:.6f}"
    )
    print(
        f"F1="
        f"{test_metrics['f1']:.6f}"
    )
    print(
        "ROC_AUC=",
        test_metrics[
            "roc_auc"
        ],
    )
    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )