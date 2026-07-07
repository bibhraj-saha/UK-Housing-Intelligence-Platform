from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from uk_housing_ml.io.csv_reader import (
    read_csv_sample_with_row_count,
)


SUPPORTED_EXTENSIONS = {".parquet", ".csv"}


@dataclass
class DatasetProfile:
    path: str
    file_name: str
    extension: str
    file_size_bytes: int
    row_count: int | None
    column_count: int | None
    columns: list[str]
    dtypes: dict[str, str]
    missingness_percent: dict[str, float]
    datetime_columns: list[str]
    datetime_ranges: dict[str, dict[str, str | None]]
    geography_columns: list[str]
    candidate_target_columns: list[str]
    leakage_risk_columns: list[str]
    derived_score_columns: list[str]
    numeric_columns: list[str]
    categorical_columns: list[str]
    duplicate_row_count: int | None
    profile_status: str
    profile_error: str | None


def load_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        raise FileNotFoundError(
            f"Readiness audit configuration not found: {config_path}"
        )

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError(
            f"Expected YAML mapping in configuration file: {config_path}"
        )

    return config


def discover_datasets(
    project_root: Path,
    config: dict[str, Any],
) -> list[Path]:
    discovery_config = config.get("discovery", {})

    configured_extensions = discovery_config.get(
        "supported_extensions",
        list(SUPPORTED_EXTENSIONS),
    )

    supported_extensions = {
        str(extension).lower()
        for extension in configured_extensions
    }

    recursive = bool(
        discovery_config.get("recursive", True)
    )

    directories = discovery_config.get(
        "directories",
        [],
    )

    discovered_paths: set[Path] = set()

    for relative_directory in directories:
        directory = project_root / relative_directory

        if not directory.exists():
            continue

        if not directory.is_dir():
            continue

        iterator = (
            directory.rglob("*")
            if recursive
            else directory.glob("*")
        )

        for path in iterator:
            if not path.is_file():
                continue

            if path.suffix.lower() not in supported_extensions:
                continue

            discovered_paths.add(path.resolve())

    return sorted(discovered_paths)


def _safe_json_value(value: Any) -> Any:
    if value is None:
        return None

    if isinstance(value, (str, bool, int)):
        return value

    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None

        return value

    if isinstance(value, pd.Timestamp):
        if pd.isna(value):
            return None

        return value.isoformat()

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    return str(value)


def _read_dataset_sample(
    dataset_path: Path,
    sample_rows: int,
) -> tuple[pd.DataFrame, int | None]:
    extension = dataset_path.suffix.lower()

    if extension == ".parquet":
        dataframe = pd.read_parquet(dataset_path)
        row_count = len(dataframe)

        if len(dataframe) > sample_rows:
            dataframe = dataframe.head(sample_rows).copy()

        return dataframe, row_count

    if extension == ".csv":
        (
            dataframe,
            row_count,
            _encoding,
        ) = read_csv_sample_with_row_count(
            dataset_path,
            sample_rows=sample_rows,
            low_memory=False,
        )

        return dataframe, row_count

    raise ValueError(
        f"Unsupported dataset extension: {extension}"
    )


def _normalise_column_name(
    column_name: str,
) -> str:
    return str(column_name).strip().lower()


def _contains_any_token(
    column_name: str,
    tokens: list[str],
) -> bool:
    normalised = _normalise_column_name(
        column_name
    )

    return any(
        str(token).lower() in normalised
        for token in tokens
    )


def _detect_datetime_columns(
    dataframe: pd.DataFrame,
    config: dict[str, Any],
) -> tuple[
    list[str],
    dict[str, dict[str, str | None]],
]:
    datetime_config = config.get(
        "datetime_detection",
        {},
    )

    name_tokens = [
        str(token).lower()
        for token in datetime_config.get(
            "name_tokens",
            [
                "date",
                "time",
                "timestamp",
                "month",
                "year",
            ],
        )
    ]

    minimum_parse_ratio = float(
        datetime_config.get(
            "minimum_parse_success_ratio",
            0.80,
        )
    )

    datetime_columns: list[str] = []
    datetime_ranges: dict[
        str,
        dict[str, str | None],
    ] = {}

    for column in dataframe.columns:
        series = dataframe[column]

        is_native_datetime = (
            pd.api.types.is_datetime64_any_dtype(
                series
            )
        )

        name_matches = _contains_any_token(
            str(column),
            name_tokens,
        )

        if not is_native_datetime and not name_matches:
            continue

        if is_native_datetime:
            parsed = pd.to_datetime(
                series,
                errors="coerce",
                utc=True,
            )
        else:
            non_null_count = int(
                series.notna().sum()
            )

            if non_null_count == 0:
                continue

            parsed = pd.to_datetime(
                series,
                errors="coerce",
                utc=True,
            )

            parse_ratio = (
                float(
                    parsed.notna().sum()
                )
                / non_null_count
            )

            if parse_ratio < minimum_parse_ratio:
                continue

        datetime_columns.append(
            str(column)
        )

        valid_values = parsed.dropna()

        minimum_value: str | None = None
        maximum_value: str | None = None

        if not valid_values.empty:
            minimum_value = (
                valid_values.min().isoformat()
            )

            maximum_value = (
                valid_values.max().isoformat()
            )

        datetime_ranges[
            str(column)
        ] = {
            "minimum": minimum_value,
            "maximum": maximum_value,
        }

    return (
        sorted(datetime_columns),
        datetime_ranges,
    )


def _detect_geography_columns(
    columns: list[str],
    config: dict[str, Any],
) -> list[str]:
    geography_tokens = [
        str(token).lower()
        for token in config.get(
            "geography_detection",
            {},
        ).get(
            "tokens",
            [
                "lsoa",
                "msoa",
                "postcode",
                "district",
                "region",
                "latitude",
                "longitude",
            ],
        )
    ]

    return sorted(
        str(column)
        for column in columns
        if _contains_any_token(
            str(column),
            geography_tokens,
        )
    )


def _detect_candidate_target_columns(
    columns: list[str],
    config: dict[str, Any],
) -> list[str]:
    target_tokens = [
        str(token).lower()
        for token in config.get(
            "target_detection",
            {},
        ).get(
            "tokens",
            [
                "price",
                "growth",
                "investment",
                "target",
                "label",
                "outcome",
            ],
        )
    ]

    return sorted(
        str(column)
        for column in columns
        if _contains_any_token(
            str(column),
            target_tokens,
        )
    )


def _detect_derived_score_columns(
    columns: list[str],
    config: dict[str, Any],
) -> list[str]:
    derived_tokens = [
        str(token).lower()
        for token in config.get(
            "derived_score_detection",
            {},
        ).get(
            "tokens",
            [
                "score",
                "rank",
                "index",
                "rating",
                "percentile",
            ],
        )
    ]

    return sorted(
        str(column)
        for column in columns
        if _contains_any_token(
            str(column),
            derived_tokens,
        )
    )


def _detect_leakage_risk_columns(
    columns: list[str],
    candidate_target_columns: list[str],
    derived_score_columns: list[str],
    config: dict[str, Any],
) -> list[str]:
    leakage_tokens = [
        str(token).lower()
        for token in config.get(
            "leakage_detection",
            {},
        ).get(
            "tokens",
            [
                "future",
                "next",
                "target",
                "label",
                "prediction",
                "predicted",
                "forecast",
                "rank",
                "score",
                "index",
            ],
        )
    ]

    detected = {
        str(column)
        for column in columns
        if _contains_any_token(
            str(column),
            leakage_tokens,
        )
    }

    detected.update(
        candidate_target_columns
    )

    detected.update(
        derived_score_columns
    )

    return sorted(detected)


def _detect_numeric_columns(
    dataframe: pd.DataFrame,
) -> list[str]:
    return sorted(
        str(column)
        for column in dataframe.select_dtypes(
            include="number"
        ).columns
    )


def _detect_categorical_columns(
    dataframe: pd.DataFrame,
) -> list[str]:
    numeric_columns = set(
        _detect_numeric_columns(
            dataframe
        )
    )

    return sorted(
        str(column)
        for column in dataframe.columns
        if str(column) not in numeric_columns
    )


def _calculate_missingness_percent(
    dataframe: pd.DataFrame,
) -> dict[str, float]:
    if dataframe.empty:
        return {
            str(column): 0.0
            for column in dataframe.columns
        }

    missingness = (
        dataframe.isna().mean() * 100.0
    )

    return {
        str(column): round(
            float(value),
            6,
        )
        for column, value in missingness.items()
    }


def profile_dataset(
    dataset_path: Path,
    project_root: Path,
    config: dict[str, Any],
) -> DatasetProfile:
    sample_rows = int(
        config.get(
            "profiling",
            {},
        ).get(
            "sample_rows",
            100000,
        )
    )

    relative_path = str(
        dataset_path.resolve().relative_to(
            project_root.resolve()
        )
    )

    try:
        dataframe, row_count = (
            _read_dataset_sample(
                dataset_path=dataset_path,
                sample_rows=sample_rows,
            )
        )

        columns = [
            str(column)
            for column in dataframe.columns
        ]

        (
            datetime_columns,
            datetime_ranges,
        ) = _detect_datetime_columns(
            dataframe=dataframe,
            config=config,
        )

        geography_columns = (
            _detect_geography_columns(
                columns=columns,
                config=config,
            )
        )

        candidate_target_columns = (
            _detect_candidate_target_columns(
                columns=columns,
                config=config,
            )
        )

        derived_score_columns = (
            _detect_derived_score_columns(
                columns=columns,
                config=config,
            )
        )

        leakage_risk_columns = (
            _detect_leakage_risk_columns(
                columns=columns,
                candidate_target_columns=(
                    candidate_target_columns
                ),
                derived_score_columns=(
                    derived_score_columns
                ),
                config=config,
            )
        )

        numeric_columns = (
            _detect_numeric_columns(
                dataframe
            )
        )

        categorical_columns = (
            _detect_categorical_columns(
                dataframe
            )
        )

        duplicate_row_count = int(
            dataframe.duplicated().sum()
        )

        return DatasetProfile(
            path=relative_path,
            file_name=dataset_path.name,
            extension=dataset_path.suffix.lower(),
            file_size_bytes=(
                dataset_path.stat().st_size
            ),
            row_count=row_count,
            column_count=len(columns),
            columns=columns,
            dtypes={
                str(column): str(dtype)
                for column, dtype
                in dataframe.dtypes.items()
            },
            missingness_percent=(
                _calculate_missingness_percent(
                    dataframe
                )
            ),
            datetime_columns=(
                datetime_columns
            ),
            datetime_ranges=(
                datetime_ranges
            ),
            geography_columns=(
                geography_columns
            ),
            candidate_target_columns=(
                candidate_target_columns
            ),
            leakage_risk_columns=(
                leakage_risk_columns
            ),
            derived_score_columns=(
                derived_score_columns
            ),
            numeric_columns=(
                numeric_columns
            ),
            categorical_columns=(
                categorical_columns
            ),
            duplicate_row_count=(
                duplicate_row_count
            ),
            profile_status="success",
            profile_error=None,
        )

    except Exception as exc:
        return DatasetProfile(
            path=relative_path,
            file_name=dataset_path.name,
            extension=dataset_path.suffix.lower(),
            file_size_bytes=(
                dataset_path.stat().st_size
            ),
            row_count=None,
            column_count=None,
            columns=[],
            dtypes={},
            missingness_percent={},
            datetime_columns=[],
            datetime_ranges={},
            geography_columns=[],
            candidate_target_columns=[],
            leakage_risk_columns=[],
            derived_score_columns=[],
            numeric_columns=[],
            categorical_columns=[],
            duplicate_row_count=None,
            profile_status="failed",
            profile_error=str(exc),
        )


def build_observed_signals(
    profiles: list[DatasetProfile],
    config: dict[str, Any],
) -> dict[str, Any]:
    successful_profiles = [
        profile
        for profile in profiles
        if profile.profile_status == "success"
    ]

    all_columns = {
        str(column).lower()
        for profile in successful_profiles
        for column in profile.columns
    }

    all_numeric_columns = {
        str(column).lower()
        for profile in successful_profiles
        for column in profile.numeric_columns
    }

    all_derived_columns = {
        str(column).lower()
        for profile in successful_profiles
        for column in profile.derived_score_columns
    }

    signal_config = config.get(
        "signal_detection",
        {},
    )

    price_tokens = [
        str(token).lower()
        for token in signal_config.get(
            "price_tokens",
            [
                "price",
                "transaction",
            ],
        )
    ]

    growth_tokens = [
        str(token).lower()
        for token in signal_config.get(
            "growth_tokens",
            [
                "growth",
                "change",
                "appreciation",
            ],
        )
    ]

    investment_tokens = [
        str(token).lower()
        for token in signal_config.get(
            "investment_tokens",
            [
                "investment",
                "yield",
                "opportunity",
            ],
        )
    ]

    has_price_signal = any(
        any(
            token in column
            for token in price_tokens
        )
        for column in all_columns
    )

    has_growth_signal = any(
        any(
            token in column
            for token in growth_tokens
        )
        for column in all_columns
    )

    has_investment_signal = any(
        any(
            token in column
            for token in investment_tokens
        )
        for column in all_columns
    )

    has_geography_signal = any(
        bool(profile.geography_columns)
        for profile in successful_profiles
    )

    has_temporal_signal = any(
        bool(profile.datetime_columns)
        for profile in successful_profiles
    )

    has_feature_signal = bool(
        all_numeric_columns
        or all_derived_columns
    )

    has_repeated_observation_signal = (
        has_temporal_signal
        and has_geography_signal
    )

    return {
        "has_datasets": bool(
            successful_profiles
        ),
        "has_price_signal": (
            has_price_signal
        ),
        "has_growth_signal": (
            has_growth_signal
        ),
        "has_investment_signal": (
            has_investment_signal
        ),
        "has_geography_signal": (
            has_geography_signal
        ),
        "has_temporal_signal": (
            has_temporal_signal
        ),
        "has_feature_signal": (
            has_feature_signal
        ),
        "has_repeated_observation_signal": (
            has_repeated_observation_signal
        ),
    }


def evaluate_task_requirements(
    task_name: str,
    task_config: dict[str, Any],
    observed_signals: dict[str, Any],
    signal_to_flag_mapping: dict[str, str],
    control_registry: dict[str, Any],
) -> dict[str, Any]:
    required_signals = [
        str(signal)
        for signal in task_config.get(
            "required_signals",
            [],
        )
    ]

    required_controls = [
        str(control)
        for control in task_config.get(
            "required_controls",
            [],
        )
    ]

    met_signals: list[str] = []
    missing_signals: list[str] = []

    for signal in required_signals:
        if signal not in signal_to_flag_mapping:
            raise KeyError(
                "Unknown signal requirement "
                f"'{signal}' for task "
                f"'{task_name}'."
            )

        observed_flag = (
            signal_to_flag_mapping[
                signal
            ]
        )

        if bool(
            observed_signals.get(
                observed_flag,
                False,
            )
        ):
            met_signals.append(signal)
        else:
            missing_signals.append(signal)

    met_controls: list[str] = []
    missing_controls: list[str] = []

    for control in required_controls:
        if control not in control_registry:
            raise KeyError(
                "Unknown engineering control "
                f"'{control}' for task "
                f"'{task_name}'."
            )

        control_definition = (
            control_registry[
                control
            ]
        )

        if not isinstance(
            control_definition,
            dict,
        ):
            raise ValueError(
                "Engineering control "
                f"'{control}' must be "
                "configured as a mapping."
            )

        if bool(
            control_definition.get(
                "satisfied",
                False,
            )
        ):
            met_controls.append(control)
        else:
            missing_controls.append(
                control
            )

    if missing_signals:
        status = "not_ready"

        reason = (
            "Required data signals are missing: "
            + ", ".join(
                missing_signals
            )
            + "."
        )

    elif missing_controls:
        status = "conditional_go"

        reason = (
            "Required data signals are present, "
            "but engineering controls remain "
            "incomplete: "
            + ", ".join(
                missing_controls
            )
            + "."
        )

    else:
        status = "go"

        reason = (
            "Required data signals and "
            "engineering controls are satisfied."
        )

    return {
        "task": task_name,
        "status": status,
        "required_signals": (
            required_signals
        ),
        "met_signals": (
            met_signals
        ),
        "missing_signals": (
            missing_signals
        ),
        "required_controls": (
            required_controls
        ),
        "met_controls": (
            met_controls
        ),
        "missing_controls": (
            missing_controls
        ),
        "reason": reason,
    }


def build_readiness_summary(
    profiles: list[DatasetProfile],
    config: dict[str, Any],
) -> dict[str, Any]:
    observed_signals = (
        build_observed_signals(
            profiles=profiles,
            config=config,
        )
    )

    readiness_config = config.get(
        "readiness",
        {},
    )

    if not isinstance(
        readiness_config,
        dict,
    ):
        readiness_config = {}

    signal_to_flag_mapping = (
        readiness_config.get(
            "signal_to_flag_mapping"
        )
    )

    if signal_to_flag_mapping is None:
        signal_to_flag_mapping = config.get(
            "signal_to_flag_mapping",
            {},
        )

    control_registry = (
        readiness_config.get(
            "control_registry"
        )
    )

    if control_registry is None:
        control_registry = config.get(
            "control_registry",
            {},
        )

    task_requirements = (
        readiness_config.get(
            "task_requirements"
        )
    )

    if task_requirements is None:
        task_requirements = config.get(
            "task_requirements",
            {},
        )

    if not isinstance(
        signal_to_flag_mapping,
        dict,
    ):
        raise ValueError(
            "signal_to_flag_mapping must be "
            "a mapping."
        )

    if not isinstance(
        control_registry,
        dict,
    ):
        raise ValueError(
            "control_registry must be "
            "a mapping."
        )

    if not isinstance(
        task_requirements,
        dict,
    ):
        raise ValueError(
            "task_requirements must be "
            "a mapping."
        )

    if not task_requirements:
        raise ValueError(
            "No task requirements were found. "
            "Expected task_requirements either "
            "under readiness.task_requirements "
            "or at the top level of the "
            "readiness audit configuration."
        )

    if not signal_to_flag_mapping:
        raise ValueError(
            "No signal-to-flag mapping was found. "
            "Expected signal_to_flag_mapping "
            "either under readiness or at the "
            "top level of the readiness audit "
            "configuration."
        )

    task_assessments = {
        str(task_name): (
            evaluate_task_requirements(
                task_name=str(
                    task_name
                ),
                task_config=(
                    task_config
                ),
                observed_signals=(
                    observed_signals
                ),
                signal_to_flag_mapping={
                    str(key): str(value)
                    for key, value
                    in signal_to_flag_mapping.items()
                },
                control_registry=(
                    control_registry
                ),
            )
        )
        for task_name, task_config
        in task_requirements.items()
    }

    return {
        "observed_signals": (
            observed_signals
        ),
        "task_assessments": (
            task_assessments
        ),
    }


def determine_overall_decision(
    task_assessments: dict[str, Any],
) -> str:
    if not task_assessments:
        return "NO_GO"

    statuses = {
        str(
            assessment.get(
                "status",
                "not_ready",
            )
        )
        for assessment
        in task_assessments.values()
    }

    if statuses == {"go"}:
        return "GO"

    if "conditional_go" in statuses:
        return "CONDITIONAL_GO"

    if "go" in statuses:
        return "CONDITIONAL_GO"

    return "NO_GO"


def _build_summary(
    profiles: list[DatasetProfile],
) -> dict[str, Any]:
    successful_profiles = [
        profile
        for profile in profiles
        if profile.profile_status == "success"
    ]

    failed_profiles = [
        profile
        for profile in profiles
        if profile.profile_status == "failed"
    ]

    temporal_dataset_count = sum(
        1
        for profile in successful_profiles
        if profile.datetime_columns
    )

    geography_dataset_count = sum(
        1
        for profile in successful_profiles
        if profile.geography_columns
    )

    candidate_target_dataset_count = sum(
        1
        for profile in successful_profiles
        if profile.candidate_target_columns
    )

    leakage_review_dataset_count = sum(
        1
        for profile in successful_profiles
        if profile.leakage_risk_columns
    )

    return {
        "dataset_count": len(profiles),
        "successful_dataset_count": len(
            successful_profiles
        ),
        "failed_dataset_count": len(
            failed_profiles
        ),
        "temporal_dataset_count": (
            temporal_dataset_count
        ),
        "geography_dataset_count": (
            geography_dataset_count
        ),
        "candidate_target_dataset_count": (
            candidate_target_dataset_count
        ),
        "leakage_review_dataset_count": (
            leakage_review_dataset_count
        ),
    }


def _build_leakage_review(
    profiles: list[DatasetProfile],
) -> list[dict[str, Any]]:
    review_items: list[
        dict[str, Any]
    ] = []

    for profile in profiles:
        if profile.profile_status != "success":
            continue

        for column in (
            profile.leakage_risk_columns
        ):
            review_items.append(
                {
                    "dataset_path": (
                        profile.path
                    ),
                    "column": column,
                    "reason": (
                        "Column name or derived "
                        "analytical role indicates "
                        "potential target leakage "
                        "and requires lineage review."
                    ),
                }
            )

    return review_items


def build_audit_report(
    project_root: Path,
    config_path: Path,
) -> dict[str, Any]:
    config = load_config(
        config_path
    )

    dataset_paths = discover_datasets(
        project_root=project_root,
        config=config,
    )

    profiles = [
        profile_dataset(
            dataset_path=dataset_path,
            project_root=project_root,
            config=config,
        )
        for dataset_path in dataset_paths
    ]

    readiness_summary = (
        build_readiness_summary(
            profiles=profiles,
            config=config,
        )
    )

    task_assessments = (
        readiness_summary[
            "task_assessments"
        ]
    )

    overall_decision = (
        determine_overall_decision(
            task_assessments
        )
    )

    return {
        "audit_metadata": {
            "project": (
                "UK Housing Intelligence Platform"
            ),
            "phase": 10,
            "audit": (
                "ML Readiness Audit"
            ),
            "generated_at_utc": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),
            "config_path": str(
                config_path.resolve().relative_to(
                    project_root.resolve()
                )
            ),
        },
        "overall_decision": (
            overall_decision
        ),
        "summary": _build_summary(
            profiles
        ),
        "observed_signals": (
            readiness_summary[
                "observed_signals"
            ]
        ),
        "task_assessments": (
            task_assessments
        ),
        "datasets": [
            asdict(profile)
            for profile in profiles
        ],
        "leakage_review": (
            _build_leakage_review(
                profiles
            )
        ),
    }


def write_json_report(
    report: dict[str, Any],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
            default=_safe_json_value,
        )
        + "\n",
        encoding="utf-8",
    )


def write_markdown_report(
    report: dict[str, Any],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    metadata = report[
        "audit_metadata"
    ]

    summary = report[
        "summary"
    ]

    task_assessments = report[
        "task_assessments"
    ]

    datasets = report[
        "datasets"
    ]

    leakage_review = report[
        "leakage_review"
    ]

    lines: list[str] = []

    lines.append(
        "# Phase 10 ML Readiness Audit"
    )
    lines.append("")

    lines.append(
        "## Audit Metadata"
    )
    lines.append("")

    lines.append(
        f"- **Project:** "
        f"{metadata['project']}"
    )

    lines.append(
        f"- **Phase:** "
        f"{metadata['phase']}"
    )

    lines.append(
        f"- **Generated at UTC:** "
        f"{metadata['generated_at_utc']}"
    )

    lines.append(
        f"- **Overall decision:** "
        f"**{report['overall_decision']}**"
    )

    lines.append("")

    lines.append(
        "## Executive Summary"
    )
    lines.append("")

    lines.append(
        f"- Datasets discovered: "
        f"{summary['dataset_count']}"
    )

    lines.append(
        f"- Successfully profiled datasets: "
        f"{summary['successful_dataset_count']}"
    )

    lines.append(
        f"- Failed dataset profiles: "
        f"{summary['failed_dataset_count']}"
    )

    lines.append(
        f"- Temporal datasets: "
        f"{summary['temporal_dataset_count']}"
    )

    lines.append(
        f"- Geography datasets: "
        f"{summary['geography_dataset_count']}"
    )

    lines.append(
        f"- Candidate-target datasets: "
        f"{summary['candidate_target_dataset_count']}"
    )

    lines.append(
        f"- Leakage-review datasets: "
        f"{summary['leakage_review_dataset_count']}"
    )

    lines.append("")

    lines.append(
        "## Observed Data Signals"
    )
    lines.append("")

    lines.append(
        "| Signal | Observed |"
    )

    lines.append(
        "|---|---|"
    )

    for (
        signal_name,
        observed,
    ) in report[
        "observed_signals"
    ].items():
        lines.append(
            f"| `{signal_name}` | "
            f"{'Yes' if observed else 'No'} |"
        )

    lines.append("")

    lines.append(
        "## Task Readiness"
    )
    lines.append("")

    lines.append(
        "| Task | Status | Missing Signals | "
        "Missing Controls |"
    )

    lines.append(
        "|---|---|---|---|"
    )

    for (
        task_name,
        assessment,
    ) in task_assessments.items():
        missing_signals = (
            ", ".join(
                assessment[
                    "missing_signals"
                ]
            )
            or "None"
        )

        missing_controls = (
            ", ".join(
                assessment[
                    "missing_controls"
                ]
            )
            or "None"
        )

        lines.append(
            f"| `{task_name}` | "
            f"{assessment['status']} | "
            f"{missing_signals} | "
            f"{missing_controls} |"
        )

    lines.append("")

    lines.append(
        "## Detailed Task Assessments"
    )
    lines.append("")

    for (
        task_name,
        assessment,
    ) in task_assessments.items():
        lines.append(
            f"### {task_name}"
        )

        lines.append("")

        lines.append(
            f"- **Status:** "
            f"{assessment['status']}"
        )

        lines.append(
            f"- **Reason:** "
            f"{assessment['reason']}"
        )

        lines.append(
            "- **Required signals:** "
            + (
                ", ".join(
                    assessment[
                        "required_signals"
                    ]
                )
                or "None"
            )
        )

        lines.append(
            "- **Met signals:** "
            + (
                ", ".join(
                    assessment[
                        "met_signals"
                    ]
                )
                or "None"
            )
        )

        lines.append(
            "- **Missing signals:** "
            + (
                ", ".join(
                    assessment[
                        "missing_signals"
                    ]
                )
                or "None"
            )
        )

        lines.append(
            "- **Required controls:** "
            + (
                ", ".join(
                    assessment[
                        "required_controls"
                    ]
                )
                or "None"
            )
        )

        lines.append(
            "- **Met controls:** "
            + (
                ", ".join(
                    assessment[
                        "met_controls"
                    ]
                )
                or "None"
            )
        )

        lines.append(
            "- **Missing controls:** "
            + (
                ", ".join(
                    assessment[
                        "missing_controls"
                    ]
                )
                or "None"
            )
        )

        lines.append("")

    lines.append(
        "## Dataset Inventory"
    )
    lines.append("")

    lines.append(
        "| Dataset | Status | Rows | Columns | "
        "Temporal | Geography | Candidate Targets |"
    )

    lines.append(
        "|---|---|---:|---:|---|---|---|"
    )

    for dataset in datasets:
        temporal = (
            ", ".join(
                dataset[
                    "datetime_columns"
                ]
            )
            or "None"
        )

        geography = (
            ", ".join(
                dataset[
                    "geography_columns"
                ]
            )
            or "None"
        )

        targets = (
            ", ".join(
                dataset[
                    "candidate_target_columns"
                ]
            )
            or "None"
        )

        lines.append(
            f"| `{dataset['path']}` | "
            f"{dataset['profile_status']} | "
            f"{dataset['row_count']} | "
            f"{dataset['column_count']} | "
            f"{temporal} | "
            f"{geography} | "
            f"{targets} |"
        )

    lines.append("")

    lines.append(
        "## Dataset Profile Failures"
    )
    lines.append("")

    failed_datasets = [
        dataset
        for dataset in datasets
        if dataset[
            "profile_status"
        ] == "failed"
    ]

    if not failed_datasets:
        lines.append(
            "No dataset profile failures were detected."
        )
    else:
        for dataset in failed_datasets:
            lines.append(
                f"- `{dataset['path']}`: "
                f"{dataset['profile_error']}"
            )

    lines.append("")

    lines.append(
        "## Leakage Review Candidates"
    )
    lines.append("")

    if not leakage_review:
        lines.append(
            "No leakage-review candidates were detected."
        )
    else:
        lines.append(
            "| Dataset | Column | Reason |"
        )

        lines.append(
            "|---|---|---|"
        )

        for item in leakage_review:
            lines.append(
                f"| `{item['dataset_path']}` | "
                f"`{item['column']}` | "
                f"{item['reason']} |"
            )

    lines.append("")

    lines.append(
        "## Leakage Interpretation"
    )
    lines.append("")

    lines.append(
        "Columns flagged by this audit are **review candidates**, "
        "not automatically confirmed leakage. Derived scores, ranks, "
        "indices, future-labelled columns, predictions, and target-like "
        "columns must be traced to their source calculations before "
        "being admitted into a training feature set."
    )

    lines.append("")

    lines.append(
        "## Architectural Decision"
    )
    lines.append("")

    lines.append(
        "Task readiness is evaluated from configuration-defined "
        "requirements. Fundamental data signals are derived from "
        "observed dataset evidence. Engineering controls are read "
        "from the control registry and remain incomplete until the "
        "corresponding Phase 10 engineering work is implemented "
        "and validated."
    )

    lines.append("")

    lines.append(
        "The ML layer must not train directly from analytical tables "
        "without explicit prediction contracts, target engineering, "
        "temporal cutoffs, and point-in-time feature validation."
    )

    lines.append("")

    lines.append(
        "## Required Next Actions"
    )
    lines.append("")

    lines.append(
        "1. Complete the predictive data-gap assessment."
    )

    lines.append(
        "2. Define prediction contracts for every ML task."
    )

    lines.append(
        "3. Define canonical geography entities and observation time."
    )

    lines.append(
        "4. Engineer future-looking targets separately from features."
    )

    lines.append(
        "5. Create a temporal leakage policy."
    )

    lines.append(
        "6. Build point-in-time-correct feature datasets."
    )

    lines.append(
        "7. Construct temporal train, validation, and test datasets."
    )

    lines.append("")

    output_path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def run_readiness_audit(
    project_root: Path,
    config_path: Path,
    json_output_path: Path,
    markdown_output_path: Path,
) -> dict[str, Any]:
    report = build_audit_report(
        project_root=project_root,
        config_path=config_path,
    )

    write_json_report(
        report=report,
        output_path=json_output_path,
    )

    write_markdown_report(
        report=report,
        output_path=markdown_output_path,
    )

    return report