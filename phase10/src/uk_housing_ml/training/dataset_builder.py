from __future__ import annotations

import json
from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
from datetime import timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from uk_housing_ml.features.leakage import (
    validate_feature_columns,
)
from uk_housing_ml.training.splitter import (
    chronological_split,
)


@dataclass(frozen=True)
class TrainingDatasetBuildResult:
    task_name: str
    target_column: str
    feature_columns: list[str]
    rejected_leakage_columns: list[str]
    total_rows: int
    train_rows: int
    validation_rows: int
    test_rows: int
    train_end_timestamp: str
    validation_end_timestamp: str
    output_directory: str


def load_contract(
    contract_path: Path,
) -> dict[str, Any]:
    if not contract_path.is_file():
        raise FileNotFoundError(
            f"Contract not found: "
            f"{contract_path}"
        )

    config = yaml.safe_load(
        contract_path.read_text(
            encoding="utf-8"
        )
    )

    if not isinstance(
        config,
        dict,
    ):
        raise ValueError(
            "Training contract must "
            "be a mapping."
        )

    contract = config.get(
        "contract"
    )

    if not isinstance(
        contract,
        dict,
    ):
        raise ValueError(
            "Missing contract mapping."
        )

    return contract


def _construct_target(
    dataframe: pd.DataFrame,
    *,
    contract: dict[str, Any],
    source_price_column: str,
) -> tuple[pd.DataFrame, str]:
    target_config = contract.get(
        "target",
        {}
    )

    target_name = str(
        target_config.get(
            "name",
            "",
        )
    )

    construction = str(
        target_config.get(
            "construction",
            "",
        )
    )

    horizon_months = int(
        target_config.get(
            "horizon_months",
            0,
        )
    )

    if not target_name:
        raise ValueError(
            "Target name is required."
        )

    if horizon_months <= 0:
        raise ValueError(
            "Target horizon_months "
            "must be positive."
        )

    entity_key = str(
        contract[
            "entity_key"
        ]
    )

    working = dataframe.copy()

    grouped_price = working.groupby(
        entity_key,
        sort=False,
    )[source_price_column]

    future_price = grouped_price.shift(
        -horizon_months
    )

    if construction == "future_shift":
        working[
            target_name
        ] = future_price

    elif (
        construction
        == "future_percentage_growth"
    ):
        current_price = working[
            source_price_column
        ]

        working[
            target_name
        ] = (
            (
                future_price
                / current_price
            )
            - 1.0
        )

    else:
        raise ValueError(
            f"Unsupported target construction: "
            f"{construction}"
        )

    return (
        working,
        target_name,
    )


def build_training_dataset(
    *,
    project_root: Path,
    feature_store_path: Path,
    contract_path: Path,
    source_price_column: str,
) -> TrainingDatasetBuildResult:
    contract = load_contract(
        contract_path
    )

    if not feature_store_path.is_file():
        raise FileNotFoundError(
            f"Feature store not found: "
            f"{feature_store_path}"
        )

    dataframe = pd.read_parquet(
        feature_store_path
    )

    task_name = str(
        contract[
            "name"
        ]
    )

    entity_key = str(
        contract[
            "entity_key"
        ]
    )

    event_timestamp = str(
        contract[
            "event_timestamp"
        ]
    )

    required_columns = {
        entity_key,
        event_timestamp,
        source_price_column,
    }

    missing_required = sorted(
        required_columns
        - set(
            dataframe.columns
        )
    )

    if missing_required:
        raise ValueError(
            "Feature store is missing "
            "required columns: "
            + ", ".join(
                missing_required
            )
        )

    dataframe = dataframe.sort_values(
        [
            entity_key,
            event_timestamp,
        ]
    ).reset_index(
        drop=True
    )

    (
        dataframe,
        target_column,
    ) = _construct_target(
        dataframe,
        contract=contract,
        source_price_column=(
            source_price_column
        ),
    )

    eligibility = contract.get(
        "eligibility",
        {}
    )

    minimum_history_periods = int(
        eligibility.get(
            "minimum_history_periods",
            1,
        )
    )

    dataframe[
        "_entity_history_periods"
    ] = (
        dataframe.groupby(
            entity_key,
            sort=False,
        )
        .cumcount()
        + 1
    )

    dataframe = dataframe[
        dataframe[
            "_entity_history_periods"
        ] >= minimum_history_periods
    ].copy()

    if bool(
        eligibility.get(
            "require_non_null_target",
            True,
        )
    ):
        dataframe = dataframe.dropna(
            subset=[
                target_column
            ]
        ).copy()

    excluded_base_columns = {
        entity_key,
        event_timestamp,
        source_price_column,
        target_column,
        "_entity_history_periods",
    }

    candidate_feature_columns = [
        str(column)
        for column in dataframe.columns
        if str(column)
        not in excluded_base_columns
    ]

    leakage_policy = contract.get(
        "leakage_policy",
        {}
    )

    leakage_result = (
        validate_feature_columns(
            candidate_feature_columns,
            target_column=target_column,
            forbidden_name_tokens=[
                str(token)
                for token in leakage_policy.get(
                    "forbidden_name_tokens",
                    [],
                )
            ],
            explicitly_forbidden_columns=[
                source_price_column
            ],
        )
    )

    feature_columns = (
        leakage_result.approved_columns
    )

    if not feature_columns:
        raise ValueError(
            "No approved feature columns "
            "remain after leakage checks."
        )

    model_dataframe = dataframe[
        [
            entity_key,
            event_timestamp,
        ]
        + feature_columns
        + [
            target_column,
        ]
    ].copy()

    split_config = contract.get(
        "split",
        {}
    )

    split_result = chronological_split(
        model_dataframe,
        timestamp_column=event_timestamp,
        train_fraction=float(
            split_config.get(
                "train_fraction",
                0.70,
            )
        ),
        validation_fraction=float(
            split_config.get(
                "validation_fraction",
                0.15,
            )
        ),
        test_fraction=float(
            split_config.get(
                "test_fraction",
                0.15,
            )
        ),
    )

    output_directory = (
        project_root
        / "phase10"
        / "data"
        / "training"
        / task_name
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    split_result.train.to_parquet(
        output_directory
        / "train.parquet",
        index=False,
    )

    split_result.validation.to_parquet(
        output_directory
        / "validation.parquet",
        index=False,
    )

    split_result.test.to_parquet(
        output_directory
        / "test.parquet",
        index=False,
    )

    result = TrainingDatasetBuildResult(
        task_name=task_name,
        target_column=target_column,
        feature_columns=feature_columns,
        rejected_leakage_columns=(
            leakage_result.rejected_columns
        ),
        total_rows=int(
            len(model_dataframe)
        ),
        train_rows=int(
            len(split_result.train)
        ),
        validation_rows=int(
            len(split_result.validation)
        ),
        test_rows=int(
            len(split_result.test)
        ),
        train_end_timestamp=(
            split_result.train_end_timestamp
        ),
        validation_end_timestamp=(
            split_result.validation_end_timestamp
        ),
        output_directory=str(
            output_directory
        ),
    )

    manifest = {
        "generated_at_utc": (
            datetime.now(
                timezone.utc
            ).isoformat()
        ),
        "contract_path": str(
            contract_path
        ),
        "feature_store_path": str(
            feature_store_path
        ),
        "result": asdict(
            result
        ),
    }

    (
        output_directory
        / "manifest.json"
    ).write_text(
        json.dumps(
            manifest,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    return result