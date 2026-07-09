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

from uk_housing_ml.features.registry import (
    FeatureDefinition,
    build_feature_registry,
)


@dataclass(frozen=True)
class FeatureStoreBuildResult:
    output_path: str
    manifest_path: str
    row_count: int
    column_count: int
    entity_count: int
    minimum_timestamp: str | None
    maximum_timestamp: str | None
    source_price_column: str
    source_transaction_column: str | None
    feature_columns: list[str]


def load_feature_store_config(
    config_path: Path,
) -> dict[str, Any]:
    if not config_path.is_file():
        raise FileNotFoundError(
            f"Feature-store config not found: "
            f"{config_path}"
        )

    config = yaml.safe_load(
        config_path.read_text(
            encoding="utf-8"
        )
    )

    if not isinstance(
        config,
        dict,
    ):
        raise ValueError(
            "Feature-store configuration "
            "must be a mapping."
        )

    return config


def _resolve_project_path(
    project_root: Path,
    configured_path: str,
) -> Path:
    path = Path(
        configured_path
    )

    if path.is_absolute():
        return path

    return (
        project_root
        / path
    )


def _select_first_existing_column(
    dataframe: pd.DataFrame,
    candidates: list[str],
    *,
    role: str,
    required: bool,
) -> str | None:
    for candidate in candidates:
        if candidate in dataframe.columns:
            return candidate

    if required:
        raise ValueError(
            f"No source column found for role "
            f"'{role}'. Candidates: "
            f"{candidates}"
        )

    return None


def _build_period_end(
    dataframe: pd.DataFrame,
    *,
    year_column: str,
    month_column: str,
) -> pd.Series:
    year = pd.to_numeric(
        dataframe[year_column],
        errors="coerce",
    )

    month = pd.to_numeric(
        dataframe[month_column],
        errors="coerce",
    )

    period_start = pd.to_datetime(
        {
            "year": year,
            "month": month,
            "day": 1,
        },
        errors="coerce",
    )

    return (
        period_start
        + pd.offsets.MonthEnd(0)
    )


def _apply_feature(
    dataframe: pd.DataFrame,
    *,
    definition: FeatureDefinition,
    entity_key: str,
    source_column: str,
) -> pd.Series:
    grouped = dataframe.groupby(
        entity_key,
        sort=False,
    )[source_column]

    if definition.operation == "lag":
        if definition.periods is None:
            raise ValueError(
                f"Feature '{definition.name}' "
                "requires periods."
            )

        return grouped.shift(
            definition.periods
        )

    if definition.operation == "pct_change":
        if definition.periods is None:
            raise ValueError(
                f"Feature '{definition.name}' "
                "requires periods."
            )

        return grouped.pct_change(
            periods=definition.periods,
            fill_method=None,
        )

    if definition.operation in {
        "rolling_mean",
        "rolling_std",
    }:
        if definition.window is None:
            raise ValueError(
                f"Feature '{definition.name}' "
                "requires window."
            )

        shift_periods = (
            definition.shift
            if definition.shift is not None
            else 1
        )

        shifted = grouped.shift(
            shift_periods
        )

        rolling = (
            shifted.groupby(
                dataframe[entity_key],
                sort=False,
            )
            .rolling(
                window=definition.window,
                min_periods=1,
            )
        )

        if (
            definition.operation
            == "rolling_mean"
        ):
            result = rolling.mean()
        else:
            result = rolling.std()

        return result.reset_index(
            level=0,
            drop=True,
        )

    raise ValueError(
        f"Unsupported feature operation "
        f"'{definition.operation}' for "
        f"feature '{definition.name}'."
    )


def build_feature_store(
    *,
    project_root: Path,
    config_path: Path,
) -> FeatureStoreBuildResult:
    config = load_feature_store_config(
        config_path
    )

    feature_store_config = config.get(
        "feature_store",
        {}
    )

    if not isinstance(
        feature_store_config,
        dict,
    ):
        raise ValueError(
            "feature_store must be a mapping."
        )

    entity_key = str(
        feature_store_config[
            "entity_key"
        ]
    )

    event_timestamp = str(
        feature_store_config[
            "event_timestamp"
        ]
    )

    source_path = _resolve_project_path(
        project_root,
        str(
            feature_store_config[
                "source_dataset"
            ]
        ),
    )

    if not source_path.is_file():
        raise FileNotFoundError(
            f"Feature source dataset "
            f"not found: {source_path}"
        )

    if source_path.suffix.lower() == ".parquet":
        dataframe = pd.read_parquet(
            source_path
        )
    elif source_path.suffix.lower() == ".csv":
        dataframe = pd.read_csv(
            source_path,
            low_memory=False,
        )
    else:
        raise ValueError(
            "Feature source must be CSV "
            "or Parquet."
        )

    source_columns = (
        feature_store_config.get(
            "source_columns",
            {}
        )
    )

    if entity_key not in dataframe.columns:
        raise ValueError(
            f"Entity key '{entity_key}' "
            "is missing from source dataset."
        )

    temporal_columns = source_columns.get(
        "temporal",
        []
    )

    if len(temporal_columns) < 2:
        raise ValueError(
            "At least year and month temporal "
            "columns must be configured."
        )

    year_column = str(
        temporal_columns[0]
    )

    month_column = str(
        temporal_columns[1]
    )

    dataframe[event_timestamp] = (
        _build_period_end(
            dataframe,
            year_column=year_column,
            month_column=month_column,
        )
    )

    dataframe = dataframe.dropna(
        subset=[
            entity_key,
            event_timestamp,
        ]
    ).copy()

    price_column = (
        _select_first_existing_column(
            dataframe,
            [
                str(column)
                for column in source_columns.get(
                    "price_candidates",
                    [],
                )
            ],
            role="price",
            required=True,
        )
    )

    transaction_column = (
        _select_first_existing_column(
            dataframe,
            [
                str(column)
                for column in source_columns.get(
                    "transaction_candidates",
                    [],
                )
            ],
            role="transaction",
            required=False,
        )
    )

    dataframe[price_column] = pd.to_numeric(
        dataframe[price_column],
        errors="coerce",
    )

    if transaction_column is not None:
        dataframe[
            transaction_column
        ] = pd.to_numeric(
            dataframe[
                transaction_column
            ],
            errors="coerce",
        )

    dataframe = dataframe.sort_values(
        [
            entity_key,
            event_timestamp,
        ]
    ).reset_index(
        drop=True
    )

    duplicate_mask = dataframe.duplicated(
        subset=[
            entity_key,
            event_timestamp,
        ],
        keep=False,
    )

    if bool(
        duplicate_mask.any()
    ):
        raise ValueError(
            "Feature-store source contains "
            "duplicate entity-timestamp rows. "
            "Expected one row per entity-month."
        )

    registry = build_feature_registry(
        config
    )

    role_to_column = {
        "price": price_column,
        "transaction": transaction_column,
    }

    feature_columns: list[str] = []

    for definition in registry:
        source_column = role_to_column.get(
            definition.source_role
        )

        if source_column is None:
            continue

        dataframe[
            definition.name
        ] = _apply_feature(
            dataframe,
            definition=definition,
            entity_key=entity_key,
            source_column=source_column,
        )

        feature_columns.append(
            definition.name
        )

    base_columns = [
        entity_key,
        event_timestamp,
        price_column,
    ]

    if transaction_column is not None:
        base_columns.append(
            transaction_column
        )

    output_dataframe = dataframe[
        base_columns
        + feature_columns
    ].copy()

    output_config = (
        feature_store_config.get(
            "output",
            {}
        )
    )

    output_path = _resolve_project_path(
        project_root,
        str(
            output_config[
                "feature_store_path"
            ]
        ),
    )

    manifest_path = _resolve_project_path(
        project_root,
        str(
            output_config[
                "manifest_path"
            ]
        ),
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_dataframe.to_parquet(
        output_path,
        index=False,
    )

    minimum_timestamp = (
        output_dataframe[
            event_timestamp
        ].min()
    )

    maximum_timestamp = (
        output_dataframe[
            event_timestamp
        ].max()
    )

    result = FeatureStoreBuildResult(
        output_path=str(
            output_path
        ),
        manifest_path=str(
            manifest_path
        ),
        row_count=int(
            len(output_dataframe)
        ),
        column_count=int(
            len(output_dataframe.columns)
        ),
        entity_count=int(
            output_dataframe[
                entity_key
            ].nunique()
        ),
        minimum_timestamp=(
            minimum_timestamp.isoformat()
            if pd.notna(
                minimum_timestamp
            )
            else None
        ),
        maximum_timestamp=(
            maximum_timestamp.isoformat()
            if pd.notna(
                maximum_timestamp
            )
            else None
        ),
        source_price_column=str(
            price_column
        ),
        source_transaction_column=(
            str(transaction_column)
            if transaction_column is not None
            else None
        ),
        feature_columns=sorted(
            feature_columns
        ),
    )

    manifest = {
        "generated_at_utc": (
            datetime.now(
                timezone.utc
            ).isoformat()
        ),
        "feature_store": (
            feature_store_config.get(
                "name"
            )
        ),
        "entity_key": entity_key,
        "event_timestamp": event_timestamp,
        "source_dataset": str(
            source_path
        ),
        "result": asdict(
            result
        ),
    }

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    return result