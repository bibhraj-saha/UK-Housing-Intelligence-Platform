"""Build Phase 10 forecasting datasets."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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


from uk_housing_ml.forecasting.dataset_builder import (  # noqa: E402
    build_forecasting_dataset,
)
from uk_housing_ml.training.splitter import (  # noqa: E402
    chronological_split,
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


def _calculate_history_months(
    frame: pd.DataFrame,
    timestamp_column: str,
) -> float:
    timestamps = pd.to_datetime(
        frame[
            timestamp_column
        ],
        errors="coerce",
    ).dropna()

    if timestamps.empty:
        return 0.0

    minimum = timestamps.min()
    maximum = timestamps.max()

    return float(
        (
            maximum
            - minimum
        ).days
        / 30.4375
    )


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

    data_config = config[
        "data"
    ]

    columns_config = config[
        "columns"
    ]

    output_config = config[
        "output"
    ]

    split_config = config[
        "split"
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

    feature_store_path = (
        _resolve_project_path(
            data_config[
                "feature_store_path"
            ]
        )
    )

    frame = pd.read_parquet(
        feature_store_path
    )

    history_months = (
        _calculate_history_months(
            frame,
            timestamp_column,
        )
    )

    dataset_directory = (
        _resolve_project_path(
            output_config[
                "dataset_directory"
            ]
        )
    )

    dataset_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest: dict[str, Any] = {
        "generated_at_utc": (
            datetime.now(
                timezone.utc
            ).isoformat()
        ),
        "task_name": config[
            "task_name"
        ],
        "source_path": str(
            feature_store_path.relative_to(
                PROJECT_ROOT
            )
        ),
        "detected_history_months": (
            history_months
        ),
        "horizons": {},
    }

    print("=" * 72)
    print(
        "PHASE 10 FORECASTING DATASET BUILD"
    )
    print("=" * 72)
    print(
        "Detected history months:",
        f"{history_months:.2f}",
    )

    for horizon_months in config[
        "horizons"
    ]:
        horizon_months = int(
            horizon_months
        )

        result = build_forecasting_dataset(
            frame,
            entity_column=entity_column,
            timestamp_column=timestamp_column,
            value_column=value_column,
            feature_columns=feature_columns,
            horizon_months=horizon_months,
        )

        if result.dataset.empty:
            manifest[
                "horizons"
            ][
                str(
                    horizon_months
                )
            ] = {
                "status": "not_feasible",
                "reason": (
                    "No complete rows remain after "
                    "forward target construction."
                ),
                "row_count": 0,
            }

            print("-" * 72)
            print(
                f"Horizon: {horizon_months} months"
            )
            print(
                "Status: not_feasible"
            )

            continue

        try:
            split_result = (
                chronological_split(
                    result.dataset,
                    timestamp_column=(
                        timestamp_column
                    ),
                    train_fraction=float(
                        split_config[
                            "train_fraction"
                        ]
                    ),
                    validation_fraction=float(
                        split_config[
                            "validation_fraction"
                        ]
                    ),
                    test_fraction=float(
                        split_config[
                            "test_fraction"
                        ]
                    ),
                )
            )
        except (TypeError, ValueError) as error:
            manifest[
                "horizons"
            ][
                str(
                    horizon_months
                )
            ] = {
                "status": "not_feasible",
                "reason": str(
                    error
                ),
                "row_count": int(
                    result.row_count
                ),
            }

            print("-" * 72)
            print(
                f"Horizon: {horizon_months} months"
            )
            print(
                "Status: not_feasible"
            )
            print(
                "Reason:",
                error,
            )

            continue

        horizon_directory = (
            dataset_directory
            / f"{horizon_months}_months"
        )

        horizon_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        full_path = (
            horizon_directory
            / "full.parquet"
        )

        train_path = (
            horizon_directory
            / "train.parquet"
        )

        validation_path = (
            horizon_directory
            / "validation.parquet"
        )

        test_path = (
            horizon_directory
            / "test.parquet"
        )

        result.dataset.to_parquet(
            full_path,
            index=False,
        )

        split_result.train.to_parquet(
            train_path,
            index=False,
        )

        split_result.validation.to_parquet(
            validation_path,
            index=False,
        )

        split_result.test.to_parquet(
            test_path,
            index=False,
        )

        manifest[
            "horizons"
        ][
            str(
                horizon_months
            )
        ] = {
            "status": "dataset_built",
            "target_column": (
                result.target_column
            ),
            "row_count": int(
                result.row_count
            ),
            "train_rows": int(
                len(
                    split_result.train
                )
            ),
            "validation_rows": int(
                len(
                    split_result.validation
                )
            ),
            "test_rows": int(
                len(
                    split_result.test
                )
            ),
            "feature_columns": (
                result.feature_columns
            ),
            "paths": {
                "full": str(
                    full_path.relative_to(
                        PROJECT_ROOT
                    )
                ),
                "train": str(
                    train_path.relative_to(
                        PROJECT_ROOT
                    )
                ),
                "validation": str(
                    validation_path.relative_to(
                        PROJECT_ROOT
                    )
                ),
                "test": str(
                    test_path.relative_to(
                        PROJECT_ROOT
                    )
                ),
            },
        }

        print("-" * 72)
        print(
            f"Horizon: {horizon_months} months"
        )
        print(
            "Status: dataset_built"
        )
        print(
            "Target:",
            result.target_column,
        )
        print(
            "Rows:",
            result.row_count,
        )
        print(
            "Train rows:",
            len(
                split_result.train
            ),
        )
        print(
            "Validation rows:",
            len(
                split_result.validation
            ),
        )
        print(
            "Test rows:",
            len(
                split_result.test
            ),
        )

    manifest_path = (
        dataset_directory
        / "forecasting_dataset_manifest.json"
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("-" * 72)
    print(
        "Manifest:",
        manifest_path,
    )
    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )