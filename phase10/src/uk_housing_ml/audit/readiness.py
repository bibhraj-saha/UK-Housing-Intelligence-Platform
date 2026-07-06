from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


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

    recursive = bool(discovery_config.get("recursive", True))
    directories = discovery_config.get("directories", [])

    discovered_paths: set[Path] = set()

    for relative_directory in directories:
        directory = project_root / relative_directory

        if not directory.exists():
            continue

        if not directory.is_dir():
            continue

        iterator = directory.rglob("*") if recursive else directory.glob("*")

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

    if pd.isna(value):
        return None

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
        dataframe = pd.read_csv(
            dataset_path,
            nrows=sample_rows,
            low_memory=False,
        )

        row_count = None

        try:
            with dataset_path.open(
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as file:
                row_count = max(sum(1 for _ in file) - 1, 0)
        except OSError:
            row_count = None

        return dataframe, row_count

    raise ValueError(
        f"Unsupported dataset extension: {extension}"
    )


def _normalise_column_name(column_name: str) -> str:
    return str(column_name).strip().lower()


def _contains_any_token(
    column_name: str,
    tokens: list[str],
) -> bool:
    normalised = _normalise_column_name(column_name)
    return any(
        token.lower() in normalised
        for token in tokens
    )


def _detect_datetime_columns(
    dataframe: pd.DataFrame,
    config: dict[str, Any],
) -> tuple[list[str], dict[str, dict[str, str | None]]]:
    datetime_config = config.get("datetime_detection", {})
    explicit_tokens = datetime_config.get(
        "explicit_name_tokens",
        [],
    )
    minimum_parse_success_ratio = float(
        datetime_config.get(
            "minimum_parse_success_ratio",
            0.90,
        )
    )

    detected_columns: list[str] = []
    ranges: dict[str, dict[str, str | None]] = {}

    for column in dataframe.columns:
        series = dataframe[column]
        normalised_name = _normalise_column_name(column)

        is_native_datetime = pd.api.types.is_datetime64_any_dtype(
            series
        )

        name_suggests_datetime = any(
            token.lower() in normalised_name
            for token in explicit_tokens
        )

        parsed_series: pd.Series | None = None

        if is_native_datetime:
            parsed_series = pd.to_datetime(
                series,
                errors="coerce",
            )

        elif name_suggests_datetime:
            non_null_series = series.dropna()

            if len(non_null_series) == 0:
                continue

            parsed_candidate = pd.to_datetime(
                non_null_series,
                errors="coerce",
            )

            parse_success_ratio = float(
                parsed_candidate.notna().mean()
            )

            if parse_success_ratio >= minimum_parse_success_ratio:
                parsed_series = pd.to_datetime(
                    series,
                    errors="coerce",
                )

        if parsed_series is None:
            continue

        detected_columns.append(str(column))

        valid_values = parsed_series.dropna()

        if valid_values.empty:
            ranges[str(column)] = {
                "min": None,
                "max": None,
            }
        else:
            ranges[str(column)] = {
                "min": _safe_json_value(valid_values.min()),
                "max": _safe_json_value(valid_values.max()),
            }

    return sorted(detected_columns), ranges


def _detect_geography_columns(
    dataframe: pd.DataFrame,
    config: dict[str, Any],
) -> list[str]:
    geography_config = config.get(
        "geography_detection",
        {},
    )

    exact_columns = {
        _normalise_column_name(column)
        for column in geography_config.get(
            "exact_columns",
            [],
        )
    }

    name_tokens = geography_config.get(
        "name_tokens",
        [],
    )

    detected: list[str] = []

    for column in dataframe.columns:
        normalised = _normalise_column_name(column)

        if normalised in exact_columns:
            detected.append(str(column))
            continue

        if _contains_any_token(str(column), name_tokens):
            detected.append(str(column))

    return sorted(set(detected))


def _detect_candidate_targets(
    dataframe: pd.DataFrame,
    config: dict[str, Any],
) -> list[str]:
    target_config = config.get(
        "candidate_target_detection",
        {},
    )

    exact_columns = {
        _normalise_column_name(column)
        for column in target_config.get(
            "exact_columns",
            [],
        )
    }

    name_tokens = target_config.get(
        "name_tokens",
        [],
    )

    detected: list[str] = []

    for column in dataframe.columns:
        normalised = _normalise_column_name(column)

        if normalised in exact_columns:
            detected.append(str(column))
            continue

        if _contains_any_token(str(column), name_tokens):
            detected.append(str(column))

    return sorted(set(detected))


def _detect_leakage_risks(
    dataframe: pd.DataFrame,
    config: dict[str, Any],
) -> tuple[list[str], list[str]]:
    leakage_config = config.get(
        "leakage_detection",
        {},
    )

    high_risk_exact_columns = {
        _normalise_column_name(column)
        for column in leakage_config.get(
            "high_risk_exact_columns",
            [],
        )
    }

    high_risk_name_tokens = leakage_config.get(
        "high_risk_name_tokens",
        [],
    )

    derived_score_tokens = leakage_config.get(
        "derived_score_tokens",
        [],
    )

    high_risk: list[str] = []
    derived_scores: list[str] = []

    for column in dataframe.columns:
        normalised = _normalise_column_name(column)

        if normalised in high_risk_exact_columns:
            high_risk.append(str(column))
        elif _contains_any_token(
            str(column),
            high_risk_name_tokens,
        ):
            high_risk.append(str(column))

        if _contains_any_token(
            str(column),
            derived_score_tokens,
        ):
            derived_scores.append(str(column))

    return (
        sorted(set(high_risk)),
        sorted(set(derived_scores)),
    )


def profile_dataset(
    dataset_path: Path,
    project_root: Path,
    config: dict[str, Any],
) -> DatasetProfile:
    profiling_config = config.get("profiling", {})
    sample_rows = int(
        profiling_config.get("sample_rows", 50000)
    )

    relative_path = str(
        dataset_path.resolve().relative_to(
            project_root.resolve()
        )
    )

    try:
        dataframe, row_count = _read_dataset_sample(
            dataset_path=dataset_path,
            sample_rows=sample_rows,
        )

        datetime_columns, datetime_ranges = (
            _detect_datetime_columns(
                dataframe=dataframe,
                config=config,
            )
        )

        geography_columns = _detect_geography_columns(
            dataframe=dataframe,
            config=config,
        )

        candidate_target_columns = _detect_candidate_targets(
            dataframe=dataframe,
            config=config,
        )

        (
            leakage_risk_columns,
            derived_score_columns,
        ) = _detect_leakage_risks(
            dataframe=dataframe,
            config=config,
        )

        numeric_columns = [
            str(column)
            for column in dataframe.select_dtypes(
                include="number"
            ).columns
        ]

        categorical_columns = [
            str(column)
            for column in dataframe.columns
            if str(column) not in numeric_columns
            and str(column) not in datetime_columns
        ]

        missingness_percent = {
            str(column): round(
                float(dataframe[column].isna().mean() * 100),
                4,
            )
            for column in dataframe.columns
        }

        duplicate_row_count = int(
            dataframe.duplicated().sum()
        )

        return DatasetProfile(
            path=relative_path,
            file_name=dataset_path.name,
            extension=dataset_path.suffix.lower(),
            file_size_bytes=dataset_path.stat().st_size,
            row_count=row_count,
            column_count=len(dataframe.columns),
            columns=[
                str(column)
                for column in dataframe.columns
            ],
            dtypes={
                str(column): str(dtype)
                for column, dtype in dataframe.dtypes.items()
            },
            missingness_percent=missingness_percent,
            datetime_columns=datetime_columns,
            datetime_ranges=datetime_ranges,
            geography_columns=geography_columns,
            candidate_target_columns=candidate_target_columns,
            leakage_risk_columns=leakage_risk_columns,
            derived_score_columns=derived_score_columns,
            numeric_columns=sorted(numeric_columns),
            categorical_columns=sorted(categorical_columns),
            duplicate_row_count=duplicate_row_count,
            profile_status="success",
            profile_error=None,
        )

    except Exception as exc:
        return DatasetProfile(
            path=relative_path,
            file_name=dataset_path.name,
            extension=dataset_path.suffix.lower(),
            file_size_bytes=dataset_path.stat().st_size,
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
            profile_error=f"{type(exc).__name__}: {exc}",
        )


def build_readiness_summary(
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

    temporal_profiles = [
        profile
        for profile in successful_profiles
        if profile.datetime_columns
    ]

    geography_profiles = [
        profile
        for profile in successful_profiles
        if profile.geography_columns
    ]

    target_profiles = [
        profile
        for profile in successful_profiles
        if profile.candidate_target_columns
    ]

    leakage_profiles = [
        profile
        for profile in successful_profiles
        if profile.leakage_risk_columns
        or profile.derived_score_columns
    ]

    price_signal_profiles = [
        profile
        for profile in successful_profiles
        if any(
            "price" in column.lower()
            for column in profile.columns
        )
    ]

    growth_signal_profiles = [
        profile
        for profile in successful_profiles
        if any(
            "growth" in column.lower()
            for column in profile.columns
        )
    ]

    investment_signal_profiles = [
        profile
        for profile in successful_profiles
        if any(
            "investment" in column.lower()
            for column in profile.columns
        )
    ]

    readiness_flags = {
        "has_datasets": len(successful_profiles) > 0,
        "has_temporal_signal": len(temporal_profiles) > 0,
        "has_geography_signal": len(geography_profiles) > 0,
        "has_candidate_targets": len(target_profiles) > 0,
        "has_price_signal": len(price_signal_profiles) > 0,
        "has_growth_signal": len(growth_signal_profiles) > 0,
        "has_investment_signal": (
            len(investment_signal_profiles) > 0
        ),
        "has_leakage_risks_to_review": (
            len(leakage_profiles) > 0
        ),
    }

    task_assessment = {
        "price_prediction": {
            "status": (
                "conditional_go"
                if readiness_flags["has_price_signal"]
                and readiness_flags["has_geography_signal"]
                and readiness_flags["has_temporal_signal"]
                else "not_ready"
            ),
            "reason": (
                "Requires a formally engineered future price target "
                "and point-in-time feature validation before training."
            ),
        },
        "growth_prediction": {
            "status": (
                "conditional_go"
                if readiness_flags["has_price_signal"]
                and readiness_flags["has_geography_signal"]
                and readiness_flags["has_temporal_signal"]
                else "not_ready"
            ),
            "reason": (
                "Requires future growth target engineering from "
                "historically ordered price observations."
            ),
        },
        "area_recommendation": {
            "status": (
                "conditional_go"
                if readiness_flags["has_geography_signal"]
                else "not_ready"
            ),
            "reason": (
                "Requires explicit user preference contracts, "
                "feature scaling, ranking logic, and offline evaluation."
            ),
        },
        "forecasting": {
            "status": (
                "conditional_go"
                if readiness_flags["has_temporal_signal"]
                else "not_ready"
            ),
            "reason": (
                "Requires repeated observations through time at a "
                "stable geography and frequency."
            ),
        },
        "investment_opportunity_prediction": {
            "status": (
                "conditional_go"
                if readiness_flags["has_investment_signal"]
                and readiness_flags["has_geography_signal"]
                and readiness_flags["has_temporal_signal"]
                else "not_ready"
            ),
            "reason": (
                "Existing investment scores are not automatically "
                "valid predictive labels. A future-outcome target "
                "must be defined."
            ),
        },
    }

    return {
        "dataset_count": len(profiles),
        "successful_dataset_count": len(successful_profiles),
        "failed_dataset_count": len(failed_profiles),
        "temporal_dataset_count": len(temporal_profiles),
        "geography_dataset_count": len(geography_profiles),
        "candidate_target_dataset_count": len(target_profiles),
        "leakage_review_dataset_count": len(leakage_profiles),
        "price_signal_dataset_count": len(price_signal_profiles),
        "growth_signal_dataset_count": len(growth_signal_profiles),
        "investment_signal_dataset_count": len(
            investment_signal_profiles
        ),
        "readiness_flags": readiness_flags,
        "task_assessment": task_assessment,
    }


def determine_overall_decision(
    summary: dict[str, Any],
) -> str:
    flags = summary["readiness_flags"]

    if not flags["has_datasets"]:
        return "NO_GO"

    if not flags["has_geography_signal"]:
        return "NO_GO"

    if not flags["has_temporal_signal"]:
        return "CONDITIONAL_GO"

    return "CONDITIONAL_GO"


def build_audit_report(
    project_root: Path,
    config_path: Path,
) -> dict[str, Any]:
    config = load_config(config_path)

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

    summary = build_readiness_summary(profiles)
    overall_decision = determine_overall_decision(summary)

    return {
        "audit_metadata": {
            "project_name": config.get(
                "project",
                {},
            ).get(
                "name",
                "UK Housing Intelligence Platform",
            ),
            "phase": config.get(
                "project",
                {},
            ).get("phase", 10),
            "audit_name": config.get(
                "project",
                {},
            ).get(
                "audit_name",
                "ML Readiness Audit",
            ),
            "generated_at_utc": datetime.now(
                timezone.utc
            ).isoformat(),
            "project_root": str(project_root.resolve()),
            "config_path": str(
                config_path.resolve().relative_to(
                    project_root.resolve()
                )
            ),
        },
        "overall_decision": overall_decision,
        "summary": summary,
        "datasets": [
            asdict(profile)
            for profile in profiles
        ],
    }


def write_json_report(
    report: dict[str, Any],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )


def _markdown_escape(value: Any) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def write_markdown_report(
    report: dict[str, Any],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    metadata = report["audit_metadata"]
    summary = report["summary"]
    task_assessment = summary["task_assessment"]

    lines: list[str] = []

    lines.append("# Phase 10 ML Readiness Audit")
    lines.append("")
    lines.append("## Audit Metadata")
    lines.append("")
    lines.append(
        f"- **Project:** {metadata['project_name']}"
    )
    lines.append(
        f"- **Phase:** {metadata['phase']}"
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

    lines.append("## Executive Summary")
    lines.append("")
    lines.append(
        f"- Discovered datasets: "
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
        f"- Datasets with temporal signals: "
        f"{summary['temporal_dataset_count']}"
    )
    lines.append(
        f"- Datasets with geography signals: "
        f"{summary['geography_dataset_count']}"
    )
    lines.append(
        f"- Datasets with candidate target signals: "
        f"{summary['candidate_target_dataset_count']}"
    )
    lines.append(
        f"- Datasets requiring leakage review: "
        f"{summary['leakage_review_dataset_count']}"
    )
    lines.append("")

    lines.append("## Task Readiness")
    lines.append("")
    lines.append("| ML Task | Status | Engineering Requirement |")
    lines.append("|---|---|---|")

    for task_name, assessment in task_assessment.items():
        lines.append(
            f"| {_markdown_escape(task_name)} "
            f"| {_markdown_escape(assessment['status'])} "
            f"| {_markdown_escape(assessment['reason'])} |"
        )

    lines.append("")
    lines.append("## Dataset Inventory")
    lines.append("")
    lines.append(
        "| Dataset | Rows | Columns | Temporal | Geography "
        "| Candidate Targets | Leakage Review | Status |"
    )
    lines.append(
        "|---|---:|---:|---|---|---|---|---|"
    )

    for dataset in report["datasets"]:
        rows = (
            dataset["row_count"]
            if dataset["row_count"] is not None
            else "unknown"
        )

        columns = (
            dataset["column_count"]
            if dataset["column_count"] is not None
            else "unknown"
        )

        temporal = ", ".join(
            dataset["datetime_columns"]
        ) or "None detected"

        geography = ", ".join(
            dataset["geography_columns"]
        ) or "None detected"

        targets = ", ".join(
            dataset["candidate_target_columns"]
        ) or "None detected"

        leakage_review_columns = sorted(
            set(
                dataset["leakage_risk_columns"]
                + dataset["derived_score_columns"]
            )
        )

        leakage_review = ", ".join(
            leakage_review_columns
        ) or "None detected"

        lines.append(
            f"| {_markdown_escape(dataset['path'])} "
            f"| {_markdown_escape(rows)} "
            f"| {_markdown_escape(columns)} "
            f"| {_markdown_escape(temporal)} "
            f"| {_markdown_escape(geography)} "
            f"| {_markdown_escape(targets)} "
            f"| {_markdown_escape(leakage_review)} "
            f"| {_markdown_escape(dataset['profile_status'])} |"
        )

    lines.append("")
    lines.append("## Leakage Interpretation")
    lines.append("")
    lines.append(
        "Columns flagged by this audit are **review candidates**, "
        "not automatically confirmed leakage. Derived scores, ranks, "
        "indices, future-labelled columns, predictions, and target-like "
        "columns must be traced to their source calculations before "
        "being admitted into a training feature set."
    )
    lines.append("")

    lines.append("## Architectural Decision")
    lines.append("")
    lines.append(
        "The ML layer must not train directly from analytical tables "
        "without explicit prediction contracts, target engineering, "
        "temporal cutoffs, and point-in-time feature validation."
    )
    lines.append("")

    lines.append("## Required Next Actions")
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