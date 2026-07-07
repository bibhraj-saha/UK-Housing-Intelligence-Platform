from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from uk_housing_ml.io.csv_reader import (
    read_csv_sample_with_row_count,
)


@dataclass
class TemporalProfile:
    column: str
    parse_success_ratio: float
    minimum_timestamp: str | None
    maximum_timestamp: str | None
    history_days: int | None
    approximate_history_months: float | None
    unique_period_count: int
    inferred_frequency: str
    median_gap_days: float | None


@dataclass
class EntityTemporalProfile:
    entity_column: str
    temporal_column: str
    unique_entity_count: int
    entity_period_pair_count: int
    entities_with_multiple_periods: int
    repeated_entity_ratio: float
    minimum_periods_per_entity: int | None
    median_periods_per_entity: float | None
    maximum_periods_per_entity: int | None
    entities_with_12_plus_periods: int
    entities_with_24_plus_periods: int
    entities_with_36_plus_periods: int
    ratio_entities_with_12_plus_periods: float
    ratio_entities_with_24_plus_periods: float
    ratio_entities_with_36_plus_periods: float


@dataclass
class DatasetGapProfile:
    path: str
    file_name: str
    extension: str
    file_size_bytes: int
    profiled_row_count: int
    total_row_count: int | None
    profile_mode: str
    columns: list[str]
    numeric_columns: list[str]
    temporal_columns: list[str]
    geography_columns: list[str]
    primary_geography_candidate: str | None
    price_columns: list[str]
    growth_columns: list[str]
    investment_columns: list[str]
    derived_analytics_columns: list[str]
    detected_feature_domains: list[str]
    missingness_percent: dict[str, float]
    temporal_profiles: list[dict[str, Any]]
    entity_temporal_profiles: list[dict[str, Any]]
    profile_status: str
    profile_error: str | None


def load_yaml_config(
    config_path: Path,
) -> dict[str, Any]:
    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    with config_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError(
            f"Expected YAML mapping in: {config_path}"
        )

    return config


def load_readiness_report(
    report_path: Path,
) -> dict[str, Any]:
    if not report_path.exists():
        raise FileNotFoundError(
            "Step 1 readiness report not found: "
            f"{report_path}"
        )

    with report_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        report = json.load(file)

    if not isinstance(report, dict):
        raise ValueError(
            f"Expected JSON object in: {report_path}"
        )

    return report


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


def _safe_float(
    value: Any,
) -> float | None:
    if value is None:
        return None

    try:
        converted = float(value)
    except (TypeError, ValueError):
        return None

    if math.isnan(converted):
        return None

    if math.isinf(converted):
        return None

    return converted


def _safe_timestamp(
    value: Any,
) -> str | None:
    if value is None:
        return None

    if pd.isna(value):
        return None

    timestamp = pd.Timestamp(value)

    return timestamp.isoformat()


def _discover_dataset_paths_from_readiness(
    project_root: Path,
    readiness_report: dict[str, Any],
) -> list[Path]:
    discovered: list[Path] = []

    for dataset in readiness_report.get(
        "datasets",
        [],
    ):
        if dataset.get("profile_status") != "success":
            continue

        relative_path = dataset.get("path")

        if not relative_path:
            continue

        path = (
            project_root
            / str(relative_path)
        ).resolve()

        if not path.exists():
            continue

        if not path.is_file():
            continue

        discovered.append(path)

    return sorted(set(discovered))


def _read_dataset_for_assessment(
    dataset_path: Path,
    sample_rows: int,
    full_profile_row_threshold: int,
) -> tuple[
    pd.DataFrame,
    int | None,
    str,
]:
    extension = dataset_path.suffix.lower()

    if extension == ".parquet":
        dataframe = pd.read_parquet(
            dataset_path
        )

        total_row_count = len(dataframe)

        if (
            total_row_count
            <= full_profile_row_threshold
        ):
            return (
                dataframe,
                total_row_count,
                "full",
            )

        sampled = dataframe.head(
            sample_rows
        ).copy()

        return (
            sampled,
            total_row_count,
            "head_sample",
        )

    if extension == ".csv":
        (
            sampled,
            total_row_count,
            _encoding,
        ) = read_csv_sample_with_row_count(
            dataset_path,
            sample_rows=sample_rows,
            low_memory=False,
        )

        profile_mode = (
            "full"
            if total_row_count <= len(sampled)
            else "head_sample"
        )

        return (
            sampled,
            total_row_count,
            profile_mode,
        )

    raise ValueError(
        f"Unsupported dataset extension: {extension}"
    )


def _detect_columns_by_config(
    dataframe: pd.DataFrame,
    exact_columns: list[str],
    name_tokens: list[str],
) -> list[str]:
    exact_set = {
        _normalise_column_name(column)
        for column in exact_columns
    }

    detected: list[str] = []

    for column in dataframe.columns:
        normalised = _normalise_column_name(
            column
        )

        if normalised in exact_set:
            detected.append(str(column))
            continue

        if _contains_any_token(
            str(column),
            name_tokens,
        ):
            detected.append(str(column))

    return sorted(set(detected))


def _detect_geography_columns(
    dataframe: pd.DataFrame,
    config: dict[str, Any],
) -> list[str]:
    geography_config = config.get(
        "geography_candidates",
        {},
    )

    exact_columns = geography_config.get(
        "exact_columns",
        [],
    )

    exact_set = {
        _normalise_column_name(column)
        for column in exact_columns
    }

    return sorted(
        {
            str(column)
            for column in dataframe.columns
            if _normalise_column_name(column)
            in exact_set
        }
    )


def _select_primary_geography_candidate(
    geography_columns: list[str],
    config: dict[str, Any],
) -> str | None:
    if not geography_columns:
        return None

    geography_config = config.get(
        "geography_candidates",
        {},
    )

    priority_order = geography_config.get(
        "priority_order",
        [],
    )

    normalised_lookup = {
        _normalise_column_name(column): column
        for column in geography_columns
    }

    for candidate in priority_order:
        normalised_candidate = (
            _normalise_column_name(candidate)
        )

        if normalised_candidate in normalised_lookup:
            return normalised_lookup[
                normalised_candidate
            ]

    return geography_columns[0]


def _detect_temporal_columns(
    dataframe: pd.DataFrame,
    config: dict[str, Any],
) -> dict[str, pd.Series]:
    temporal_config = config.get(
        "temporal_detection",
        {},
    )

    explicit_tokens = temporal_config.get(
        "explicit_name_tokens",
        [],
    )

    minimum_parse_success_ratio = float(
        temporal_config.get(
            "minimum_parse_success_ratio",
            0.90,
        )
    )

    detected: dict[str, pd.Series] = {}

    for column in dataframe.columns:
        series = dataframe[column]

        is_native_datetime = (
            pd.api.types.is_datetime64_any_dtype(
                series
            )
        )

        name_suggests_datetime = (
            _contains_any_token(
                str(column),
                explicit_tokens,
            )
        )

        if not (
            is_native_datetime
            or name_suggests_datetime
        ):
            continue

        parsed = pd.to_datetime(
            series,
            errors="coerce",
        )

        non_null_original = int(
            series.notna().sum()
        )

        if non_null_original == 0:
            continue

        parse_success_ratio = float(
            parsed.notna().sum()
            / non_null_original
        )

        if (
            parse_success_ratio
            < minimum_parse_success_ratio
        ):
            continue

        detected[str(column)] = parsed

    return detected


def _infer_frequency(
    parsed_series: pd.Series,
) -> tuple[str, float | None]:
    valid = (
        parsed_series
        .dropna()
        .drop_duplicates()
        .sort_values()
    )

    if len(valid) < 2:
        return "insufficient_observations", None

    differences = (
        valid.diff()
        .dropna()
        .dt.total_seconds()
        / 86400.0
    )

    if differences.empty:
        return "insufficient_observations", None

    median_gap_days = float(
        differences.median()
    )

    if median_gap_days <= 2:
        frequency = "daily_or_transactional"

    elif median_gap_days <= 10:
        frequency = "weekly"

    elif median_gap_days <= 45:
        frequency = "monthly"

    elif median_gap_days <= 120:
        frequency = "quarterly"

    elif median_gap_days <= 400:
        frequency = "annual"

    else:
        frequency = "irregular_or_sparse"

    return (
        frequency,
        round(median_gap_days, 4),
    )


def _build_temporal_profile(
    column_name: str,
    original_series: pd.Series,
    parsed_series: pd.Series,
) -> TemporalProfile:
    non_null_original = int(
        original_series.notna().sum()
    )

    parse_success_ratio = (
        float(
            parsed_series.notna().sum()
            / non_null_original
        )
        if non_null_original > 0
        else 0.0
    )

    valid = parsed_series.dropna()

    if valid.empty:
        minimum_timestamp = None
        maximum_timestamp = None
        history_days = None
        approximate_history_months = None
        unique_period_count = 0

    else:
        minimum_value = valid.min()
        maximum_value = valid.max()

        minimum_timestamp = _safe_timestamp(
            minimum_value
        )

        maximum_timestamp = _safe_timestamp(
            maximum_value
        )

        history_days = int(
            (
                maximum_value
                - minimum_value
            ).days
        )

        approximate_history_months = round(
            history_days / 30.4375,
            2,
        )

        unique_period_count = int(
            valid.nunique()
        )

    (
        inferred_frequency,
        median_gap_days,
    ) = _infer_frequency(
        parsed_series
    )

    return TemporalProfile(
        column=column_name,
        parse_success_ratio=round(
            parse_success_ratio,
            6,
        ),
        minimum_timestamp=minimum_timestamp,
        maximum_timestamp=maximum_timestamp,
        history_days=history_days,
        approximate_history_months=(
            approximate_history_months
        ),
        unique_period_count=(
            unique_period_count
        ),
        inferred_frequency=(
            inferred_frequency
        ),
        median_gap_days=median_gap_days,
    )


def _build_entity_temporal_profile(
    dataframe: pd.DataFrame,
    entity_column: str,
    temporal_column: str,
    parsed_temporal_series: pd.Series,
) -> EntityTemporalProfile:
    working = pd.DataFrame(
        {
            "entity": dataframe[
                entity_column
            ],
            "timestamp": parsed_temporal_series,
        }
    )

    working = working.dropna(
        subset=[
            "entity",
            "timestamp",
        ]
    )

    if working.empty:
        return EntityTemporalProfile(
            entity_column=entity_column,
            temporal_column=temporal_column,
            unique_entity_count=0,
            entity_period_pair_count=0,
            entities_with_multiple_periods=0,
            repeated_entity_ratio=0.0,
            minimum_periods_per_entity=None,
            median_periods_per_entity=None,
            maximum_periods_per_entity=None,
            entities_with_12_plus_periods=0,
            entities_with_24_plus_periods=0,
            entities_with_36_plus_periods=0,
            ratio_entities_with_12_plus_periods=0.0,
            ratio_entities_with_24_plus_periods=0.0,
            ratio_entities_with_36_plus_periods=0.0,
        )

    working["period"] = (
        working["timestamp"]
        .dt.tz_localize(None)
        .dt.to_period("M")
        .astype(str)
    )

    entity_periods = (
        working[
            [
                "entity",
                "period",
            ]
        ]
        .drop_duplicates()
    )

    periods_per_entity = (
        entity_periods
        .groupby("entity")
        .size()
    )

    unique_entity_count = int(
        periods_per_entity.shape[0]
    )

    entity_period_pair_count = int(
        len(entity_periods)
    )

    entities_with_multiple_periods = int(
        (periods_per_entity >= 2).sum()
    )

    repeated_entity_ratio = (
        float(
            entities_with_multiple_periods
            / unique_entity_count
        )
        if unique_entity_count > 0
        else 0.0
    )

    entities_with_12_plus_periods = int(
        (periods_per_entity >= 12).sum()
    )

    entities_with_24_plus_periods = int(
        (periods_per_entity >= 24).sum()
    )

    entities_with_36_plus_periods = int(
        (periods_per_entity >= 36).sum()
    )

    def ratio(
        numerator: int,
    ) -> float:
        if unique_entity_count == 0:
            return 0.0

        return float(
            numerator
            / unique_entity_count
        )

    return EntityTemporalProfile(
        entity_column=entity_column,
        temporal_column=temporal_column,
        unique_entity_count=(
            unique_entity_count
        ),
        entity_period_pair_count=(
            entity_period_pair_count
        ),
        entities_with_multiple_periods=(
            entities_with_multiple_periods
        ),
        repeated_entity_ratio=round(
            repeated_entity_ratio,
            6,
        ),
        minimum_periods_per_entity=int(
            periods_per_entity.min()
        ),
        median_periods_per_entity=round(
            float(
                periods_per_entity.median()
            ),
            4,
        ),
        maximum_periods_per_entity=int(
            periods_per_entity.max()
        ),
        entities_with_12_plus_periods=(
            entities_with_12_plus_periods
        ),
        entities_with_24_plus_periods=(
            entities_with_24_plus_periods
        ),
        entities_with_36_plus_periods=(
            entities_with_36_plus_periods
        ),
        ratio_entities_with_12_plus_periods=round(
            ratio(
                entities_with_12_plus_periods
            ),
            6,
        ),
        ratio_entities_with_24_plus_periods=round(
            ratio(
                entities_with_24_plus_periods
            ),
            6,
        ),
        ratio_entities_with_36_plus_periods=round(
            ratio(
                entities_with_36_plus_periods
            ),
            6,
        ),
    )


def _detect_feature_domains(
    dataframe: pd.DataFrame,
    config: dict[str, Any],
) -> list[str]:
    domain_config = config.get(
        "feature_domain_detection",
        {},
    )

    detected_domains: list[str] = []

    for domain_name, domain_rules in (
        domain_config.items()
    ):
        tokens = domain_rules.get(
            "tokens",
            [],
        )

        domain_detected = any(
            _contains_any_token(
                str(column),
                tokens,
            )
            for column in dataframe.columns
        )

        if domain_detected:
            detected_domains.append(
                str(domain_name)
            )

    return sorted(
        set(detected_domains)
    )


def profile_dataset_for_gaps(
    dataset_path: Path,
    project_root: Path,
    config: dict[str, Any],
) -> DatasetGapProfile:
    assessment_config = config.get(
        "assessment",
        {},
    )

    sample_rows = int(
        assessment_config.get(
            "sample_rows_per_dataset",
            250000,
        )
    )

    full_profile_row_threshold = int(
        assessment_config.get(
            "full_profile_row_threshold",
            500000,
        )
    )

    relative_path = str(
        dataset_path
        .resolve()
        .relative_to(
            project_root.resolve()
        )
    )

    try:
        (
            dataframe,
            total_row_count,
            profile_mode,
        ) = _read_dataset_for_assessment(
            dataset_path=dataset_path,
            sample_rows=sample_rows,
            full_profile_row_threshold=(
                full_profile_row_threshold
            ),
        )

        temporal_series = (
            _detect_temporal_columns(
                dataframe=dataframe,
                config=config,
            )
        )

        temporal_profiles = [
            asdict(
                _build_temporal_profile(
                    column_name=column_name,
                    original_series=(
                        dataframe[column_name]
                    ),
                    parsed_series=parsed_series,
                )
            )
            for column_name, parsed_series
            in temporal_series.items()
        ]

        geography_columns = (
            _detect_geography_columns(
                dataframe=dataframe,
                config=config,
            )
        )

        primary_geography_candidate = (
            _select_primary_geography_candidate(
                geography_columns=(
                    geography_columns
                ),
                config=config,
            )
        )

        price_config = config.get(
            "price_detection",
            {},
        )

        price_columns = (
            _detect_columns_by_config(
                dataframe=dataframe,
                exact_columns=price_config.get(
                    "exact_columns",
                    [],
                ),
                name_tokens=price_config.get(
                    "name_tokens",
                    [],
                ),
            )
        )

        growth_config = config.get(
            "growth_detection",
            {},
        )

        growth_columns = (
            _detect_columns_by_config(
                dataframe=dataframe,
                exact_columns=growth_config.get(
                    "exact_columns",
                    [],
                ),
                name_tokens=growth_config.get(
                    "name_tokens",
                    [],
                ),
            )
        )

        investment_config = config.get(
            "investment_detection",
            {},
        )

        investment_columns = (
            _detect_columns_by_config(
                dataframe=dataframe,
                exact_columns=(
                    investment_config.get(
                        "exact_columns",
                        [],
                    )
                ),
                name_tokens=(
                    investment_config.get(
                        "name_tokens",
                        [],
                    )
                ),
            )
        )

        derived_config = config.get(
            "derived_analytics_detection",
            {},
        )

        derived_analytics_columns = (
            _detect_columns_by_config(
                dataframe=dataframe,
                exact_columns=[],
                name_tokens=derived_config.get(
                    "name_tokens",
                    [],
                ),
            )
        )

        detected_feature_domains = (
            _detect_feature_domains(
                dataframe=dataframe,
                config=config,
            )
        )

        numeric_columns = [
            str(column)
            for column
            in dataframe.select_dtypes(
                include="number"
            ).columns
        ]

        missingness_percent = {
            str(column): round(
                float(
                    dataframe[column]
                    .isna()
                    .mean()
                    * 100
                ),
                4,
            )
            for column in dataframe.columns
        }

        entity_temporal_profiles: list[
            dict[str, Any]
        ] = []

        if primary_geography_candidate:
            for (
                temporal_column,
                parsed_series,
            ) in temporal_series.items():
                entity_temporal_profiles.append(
                    asdict(
                        _build_entity_temporal_profile(
                            dataframe=dataframe,
                            entity_column=(
                                primary_geography_candidate
                            ),
                            temporal_column=(
                                temporal_column
                            ),
                            parsed_temporal_series=(
                                parsed_series
                            ),
                        )
                    )
                )

        return DatasetGapProfile(
            path=relative_path,
            file_name=dataset_path.name,
            extension=dataset_path.suffix.lower(),
            file_size_bytes=(
                dataset_path.stat().st_size
            ),
            profiled_row_count=len(dataframe),
            total_row_count=total_row_count,
            profile_mode=profile_mode,
            columns=[
                str(column)
                for column in dataframe.columns
            ],
            numeric_columns=sorted(
                numeric_columns
            ),
            temporal_columns=sorted(
                temporal_series.keys()
            ),
            geography_columns=(
                geography_columns
            ),
            primary_geography_candidate=(
                primary_geography_candidate
            ),
            price_columns=price_columns,
            growth_columns=growth_columns,
            investment_columns=(
                investment_columns
            ),
            derived_analytics_columns=(
                derived_analytics_columns
            ),
            detected_feature_domains=(
                detected_feature_domains
            ),
            missingness_percent=(
                missingness_percent
            ),
            temporal_profiles=(
                temporal_profiles
            ),
            entity_temporal_profiles=(
                entity_temporal_profiles
            ),
            profile_status="success",
            profile_error=None,
        )

    except Exception as exc:
        return DatasetGapProfile(
            path=relative_path,
            file_name=dataset_path.name,
            extension=dataset_path.suffix.lower(),
            file_size_bytes=(
                dataset_path.stat().st_size
            ),
            profiled_row_count=0,
            total_row_count=None,
            profile_mode="failed",
            columns=[],
            numeric_columns=[],
            temporal_columns=[],
            geography_columns=[],
            primary_geography_candidate=None,
            price_columns=[],
            growth_columns=[],
            investment_columns=[],
            derived_analytics_columns=[],
            detected_feature_domains=[],
            missingness_percent={},
            temporal_profiles=[],
            entity_temporal_profiles=[],
            profile_status="failed",
            profile_error=(
                f"{type(exc).__name__}: {exc}"
            ),
        )


def _aggregate_available_domains(
    profiles: list[DatasetGapProfile],
) -> list[str]:
    domains: set[str] = set()

    for profile in profiles:
        if profile.profile_status != "success":
            continue

        domains.update(
            profile.detected_feature_domains
        )

    return sorted(domains)


def _maximum_history_months(
    profiles: list[DatasetGapProfile],
) -> float | None:
    values: list[float] = []

    for profile in profiles:
        if profile.profile_status != "success":
            continue

        has_price_signal = bool(
            profile.price_columns
        )

        has_geography_signal = bool(
            profile.geography_columns
        )

        if not (
            has_price_signal
            and has_geography_signal
        ):
            continue

        for temporal_profile in (
            profile.temporal_profiles
        ):
            history_months = (
                temporal_profile.get(
                    "approximate_history_months"
                )
            )

            safe_value = _safe_float(
                history_months
            )

            if safe_value is not None:
                values.append(
                    safe_value
                )

    if not values:
        return None

    return max(values)


def _best_entity_temporal_profile(
    profiles: list[DatasetGapProfile],
) -> dict[str, Any] | None:
    candidates: list[dict[str, Any]] = []

    for profile in profiles:
        if profile.profile_status != "success":
            continue

        for entity_profile in (
            profile.entity_temporal_profiles
        ):
            candidate = dict(
                entity_profile
            )

            candidate["dataset_path"] = (
                profile.path
            )

            candidates.append(candidate)

    if not candidates:
        return None

    return max(
        candidates,
        key=lambda item: (
            float(
                item.get(
                    "repeated_entity_ratio",
                    0.0,
                )
            ),
            int(
                item.get(
                    "unique_entity_count",
                    0,
                )
            ),
            float(
                item.get(
                    "median_periods_per_entity",
                    0.0,
                )
                or 0.0
            ),
        ),
    )


def _assess_horizon_feasibility(
    maximum_history_months: float | None,
    horizons: list[int],
) -> dict[str, dict[str, Any]]:
    results: dict[
        str,
        dict[str, Any],
    ] = {}

    for horizon in horizons:
        key = f"{horizon}_months"

        if maximum_history_months is None:
            results[key] = {
                "status": "not_evaluable",
                "reason": (
                    "No measurable temporal history "
                    "was detected."
                ),
            }

            continue

        if maximum_history_months < horizon:
            results[key] = {
                "status": "not_feasible",
                "reason": (
                    "Maximum detected history "
                    f"({maximum_history_months:.2f} months) "
                    f"is shorter than the {horizon}-month "
                    "horizon."
                ),
            }

            continue

        if maximum_history_months < (
            horizon * 2
        ):
            results[key] = {
                "status": "weakly_feasible",
                "reason": (
                    "Detected history exceeds the target "
                    "horizon but provides limited room for "
                    "training, validation, and testing."
                ),
            }

            continue

        results[key] = {
            "status": "structurally_feasible",
            "reason": (
                "Detected history is at least twice the "
                "candidate horizon. Entity-level coverage "
                "and point-in-time target construction still "
                "require validation."
            ),
        }

    return results


def _assess_task_gaps(
    task_name: str,
    task_config: dict[str, Any],
    available_domains: list[str],
    maximum_history_months: float | None,
    best_entity_temporal_profile: (
        dict[str, Any] | None
    ),
    config: dict[str, Any],
) -> dict[str, Any]:
    required_domains = task_config.get(
        "required_domains",
        [],
    )

    recommended_domains = task_config.get(
        "recommended_domains",
        [],
    )

    missing_required_domains = [
        domain
        for domain in required_domains
        if domain not in available_domains
    ]

    missing_recommended_domains = [
        domain
        for domain in recommended_domains
        if domain not in available_domains
    ]

    assessment_config = config.get(
        "assessment",
        {},
    )

    minimum_history_by_task = (
        assessment_config.get(
            "minimum_history_months",
            {},
        )
    )

    required_history_months = (
        minimum_history_by_task.get(
            task_name
        )
    )

    history_gap = False

    if required_history_months is not None:
        history_gap = (
            maximum_history_months is None
            or maximum_history_months
            < float(required_history_months)
        )

    minimum_periods_by_task = (
        assessment_config.get(
            "minimum_periods_per_entity",
            {},
        )
    )

    required_periods_per_entity = (
        minimum_periods_by_task.get(
            task_name
        )
    )

    entity_coverage_gap = False

    if required_periods_per_entity is not None:
        if best_entity_temporal_profile is None:
            entity_coverage_gap = True
        else:
            median_periods = _safe_float(
                best_entity_temporal_profile.get(
                    "median_periods_per_entity"
                )
            )

            entity_coverage_gap = (
                median_periods is None
                or median_periods
                < float(
                    required_periods_per_entity
                )
            )

    gaps: list[dict[str, Any]] = []

    for domain in missing_required_domains:
        gaps.append(
            {
                "gap_type": "missing_required_domain",
                "severity": "blocking",
                "detail": (
                    f"Required domain '{domain}' "
                    f"is not detected for task "
                    f"'{task_name}'."
                ),
            }
        )

    for domain in missing_recommended_domains:
        gaps.append(
            {
                "gap_type": (
                    "recommended_domain_missing"
                ),
                "severity": "medium",
                "detail": (
                    f"Recommended domain '{domain}' "
                    f"is not detected for task "
                    f"'{task_name}'."
                ),
            }
        )

    if history_gap:
        gaps.append(
            {
                "gap_type": "insufficient_history",
                "severity": "high",
                "detail": (
                    f"Task requires approximately "
                    f"{required_history_months} months "
                    "of history, but detected maximum "
                    f"history is {maximum_history_months}."
                ),
            }
        )

    if entity_coverage_gap:
        gaps.append(
            {
                "gap_type": (
                    "insufficient_repeated_entity_coverage"
                ),
                "severity": "high",
                "detail": (
                    "The best detected entity-temporal "
                    "candidate does not meet the configured "
                    "median periods-per-entity requirement "
                    f"of {required_periods_per_entity}."
                ),
            }
        )

    target_requirement = task_config.get(
        "target_requirement",
        {},
    )

    target_type = target_requirement.get(
        "target_type"
    )

    requires_future_horizon = bool(
        target_requirement.get(
            "requires_future_horizon",
            False,
        )
    )

    if requires_future_horizon:
        gaps.append(
            {
                "gap_type": (
                    "future_target_not_defined"
                ),
                "severity": "high",
                "detail": (
                    f"Future target '{target_type}' "
                    "has not yet been formally defined "
                    "through a prediction contract."
                ),
            }
        )

    if missing_required_domains:
        status = "blocked"

    elif history_gap or entity_coverage_gap:
        status = "major_gaps"

    elif requires_future_horizon:
        status = "engineering_required"

    else:
        status = "candidate_ready"

    return {
        "status": status,
        "required_domains": required_domains,
        "available_required_domains": [
            domain
            for domain in required_domains
            if domain in available_domains
        ],
        "missing_required_domains": (
            missing_required_domains
        ),
        "recommended_domains": (
            recommended_domains
        ),
        "missing_recommended_domains": (
            missing_recommended_domains
        ),
        "required_history_months": (
            required_history_months
        ),
        "detected_maximum_history_months": (
            maximum_history_months
        ),
        "required_median_periods_per_entity": (
            required_periods_per_entity
        ),
        "target_requirement": (
            target_requirement
        ),
        "gaps": gaps,
    }


def _assess_derived_target_risks(
    profiles: list[DatasetGapProfile],
) -> list[dict[str, Any]]:
    risks: list[dict[str, Any]] = []

    for profile in profiles:
        if profile.profile_status != "success":
            continue

        for column in (
            profile.derived_analytics_columns
        ):
            normalised = column.lower()

            if (
                "growth" in normalised
                or "investment" in normalised
                or "index" in normalised
                or "rank" in normalised
            ):
                risks.append(
                    {
                        "dataset_path": profile.path,
                        "column": column,
                        "risk_type": (
                            "derived_score_target_risk"
                        ),
                        "severity": "high",
                        "detail": (
                            "Derived analytical columns must "
                            "not automatically be used as "
                            "predictive labels or leakage-safe "
                            "features without lineage review."
                        ),
                    }
                )

    return risks


def _build_domain_inventory(
    profiles: list[DatasetGapProfile],
) -> dict[str, list[str]]:
    inventory: dict[str, list[str]] = {}

    for profile in profiles:
        if profile.profile_status != "success":
            continue

        for domain in (
            profile.detected_feature_domains
        ):
            inventory.setdefault(
                domain,
                [],
            ).append(
                profile.path
            )

    return {
        domain: sorted(
            set(paths)
        )
        for domain, paths
        in sorted(inventory.items())
    }


def _build_column_frequency(
    profiles: list[DatasetGapProfile],
) -> dict[str, int]:
    counter: Counter[str] = Counter()

    for profile in profiles:
        if profile.profile_status != "success":
            continue

        counter.update(
            profile.columns
        )

    return dict(
        sorted(
            counter.items(),
            key=lambda item: (
                -item[1],
                item[0],
            ),
        )
    )


def build_predictive_data_gap_report(
    project_root: Path,
    config_path: Path,
    readiness_report_path: Path,
) -> dict[str, Any]:
    config = load_yaml_config(
        config_path
    )

    readiness_report = (
        load_readiness_report(
            readiness_report_path
        )
    )

    dataset_paths = (
        _discover_dataset_paths_from_readiness(
            project_root=project_root,
            readiness_report=readiness_report,
        )
    )

    profiles = [
        profile_dataset_for_gaps(
            dataset_path=dataset_path,
            project_root=project_root,
            config=config,
        )
        for dataset_path in dataset_paths
    ]

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

    available_domains = (
        _aggregate_available_domains(
            successful_profiles
        )
    )

    maximum_history_months = (
        _maximum_history_months(
            successful_profiles
        )
    )

    best_entity_temporal_profile = (
        _best_entity_temporal_profile(
            successful_profiles
        )
    )

    assessment_config = config.get(
        "assessment",
        {},
    )

    candidate_horizons = [
        int(value)
        for value in assessment_config.get(
            "candidate_horizons_months",
            [
                3,
                6,
                12,
                24,
            ],
        )
    ]

    horizon_feasibility = (
        _assess_horizon_feasibility(
            maximum_history_months=(
                maximum_history_months
            ),
            horizons=candidate_horizons,
        )
    )

    task_requirements = config.get(
        "task_requirements",
        {},
    )

    task_assessments = {
        task_name: _assess_task_gaps(
            task_name=task_name,
            task_config=task_config,
            available_domains=(
                available_domains
            ),
            maximum_history_months=(
                maximum_history_months
            ),
            best_entity_temporal_profile=(
                best_entity_temporal_profile
            ),
            config=config,
        )
        for task_name, task_config
        in task_requirements.items()
    }

    derived_target_risks = (
        _assess_derived_target_risks(
            successful_profiles
        )
    )

    domain_inventory = (
        _build_domain_inventory(
            successful_profiles
        )
    )

    column_frequency = (
        _build_column_frequency(
            successful_profiles
        )
    )

    status_counts = Counter(
        assessment["status"]
        for assessment
        in task_assessments.values()
    )

    if status_counts.get(
        "blocked",
        0,
    ) > 0:
        overall_decision = (
            "CONDITIONAL_GO_WITH_BLOCKED_TASKS"
        )

    elif status_counts.get(
        "major_gaps",
        0,
    ) > 0:
        overall_decision = (
            "CONDITIONAL_GO_WITH_MAJOR_GAPS"
        )

    elif status_counts.get(
        "engineering_required",
        0,
    ) > 0:
        overall_decision = (
            "CONDITIONAL_GO_ENGINEERING_REQUIRED"
        )

    else:
        overall_decision = "GO"

    return {
        "assessment_metadata": {
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
            ).get(
                "phase",
                10,
            ),
            "assessment_name": config.get(
                "project",
                {},
            ).get(
                "assessment_name",
                "Predictive Data-Gap Assessment",
            ),
            "generated_at_utc": datetime.now(
                timezone.utc
            ).isoformat(),
            "project_root": str(
                project_root.resolve()
            ),
            "config_path": str(
                config_path
                .resolve()
                .relative_to(
                    project_root.resolve()
                )
            ),
            "readiness_report_path": str(
                readiness_report_path
                .resolve()
                .relative_to(
                    project_root.resolve()
                )
            ),
        },
        "overall_decision": overall_decision,
        "summary": {
            "dataset_count": len(profiles),
            "successful_dataset_count": len(
                successful_profiles
            ),
            "failed_dataset_count": len(
                failed_profiles
            ),
            "available_domains": (
                available_domains
            ),
            "maximum_detected_history_months": (
                maximum_history_months
            ),
            "best_entity_temporal_profile": (
                best_entity_temporal_profile
            ),
            "task_status_counts": dict(
                status_counts
            ),
        },
        "horizon_feasibility": (
            horizon_feasibility
        ),
        "task_assessments": (
            task_assessments
        ),
        "derived_target_risks": (
            derived_target_risks
        ),
        "domain_inventory": (
            domain_inventory
        ),
        "column_frequency": (
            column_frequency
        ),
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


def _markdown_escape(
    value: Any,
) -> str:
    return (
        str(value)
        .replace("|", "\\|")
        .replace("\n", " ")
    )


def _format_items(
    items: list[str],
) -> str:
    if not items:
        return "None"

    return ", ".join(items)


def write_markdown_report(
    report: dict[str, Any],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    metadata = report[
        "assessment_metadata"
    ]

    summary = report["summary"]

    lines: list[str] = []

    lines.append(
        "# Phase 10 Predictive Data-Gap Assessment"
    )
    lines.append("")

    lines.append("## Assessment Metadata")
    lines.append("")

    lines.append(
        f"- **Project:** "
        f"{metadata['project_name']}"
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

    lines.append("## Executive Summary")
    lines.append("")

    lines.append(
        f"- Datasets assessed: "
        f"{summary['dataset_count']}"
    )

    lines.append(
        f"- Successfully assessed datasets: "
        f"{summary['successful_dataset_count']}"
    )

    lines.append(
        f"- Failed dataset assessments: "
        f"{summary['failed_dataset_count']}"
    )

    lines.append(
        f"- Available feature domains: "
        f"{_format_items(summary['available_domains'])}"
    )

    lines.append(
        f"- Maximum detected history in months: "
        f"{summary['maximum_detected_history_months']}"
    )

    lines.append("")

    lines.append(
        "## Candidate Horizon Feasibility"
    )
    lines.append("")

    lines.append(
        "| Horizon | Status | Reason |"
    )
    lines.append(
        "|---|---|---|"
    )

    for horizon, assessment in (
        report[
            "horizon_feasibility"
        ].items()
    ):
        lines.append(
            f"| {_markdown_escape(horizon)} "
            f"| {_markdown_escape(assessment['status'])} "
            f"| {_markdown_escape(assessment['reason'])} |"
        )

    lines.append("")

    lines.append("## Task Assessments")
    lines.append("")

    lines.append(
        "| Task | Status | Missing Required Domains "
        "| Missing Recommended Domains |"
    )

    lines.append(
        "|---|---|---|---|"
    )

    for task_name, assessment in (
        report[
            "task_assessments"
        ].items()
    ):
        lines.append(
            f"| {_markdown_escape(task_name)} "
            f"| {_markdown_escape(assessment['status'])} "
            f"| {_markdown_escape(_format_items(assessment['missing_required_domains']))} "
            f"| {_markdown_escape(_format_items(assessment['missing_recommended_domains']))} |"
        )

    lines.append("")

    lines.append(
        "## Detailed Task Gaps"
    )
    lines.append("")

    for task_name, assessment in (
        report[
            "task_assessments"
        ].items()
    ):
        lines.append(
            f"### {task_name}"
        )
        lines.append("")

        lines.append(
            f"- **Status:** "
            f"{assessment['status']}"
        )

        lines.append(
            f"- **Required domains:** "
            f"{_format_items(assessment['required_domains'])}"
        )

        lines.append(
            f"- **Available required domains:** "
            f"{_format_items(assessment['available_required_domains'])}"
        )

        lines.append(
            f"- **Missing required domains:** "
            f"{_format_items(assessment['missing_required_domains'])}"
        )

        lines.append(
            f"- **Missing recommended domains:** "
            f"{_format_items(assessment['missing_recommended_domains'])}"
        )

        lines.append(
            f"- **Required history months:** "
            f"{assessment['required_history_months']}"
        )

        lines.append(
            f"- **Detected maximum history months:** "
            f"{assessment['detected_maximum_history_months']}"
        )

        lines.append(
            f"- **Required median periods per entity:** "
            f"{assessment['required_median_periods_per_entity']}"
        )

        lines.append("")

        lines.append("#### Gaps")
        lines.append("")

        gaps = assessment["gaps"]

        if not gaps:
            lines.append(
                "- No configured gaps detected."
            )
        else:
            for gap in gaps:
                lines.append(
                    f"- **{gap['severity']} — "
                    f"{gap['gap_type']}:** "
                    f"{gap['detail']}"
                )

        lines.append("")

    lines.append(
        "## Best Entity-Temporal Candidate"
    )
    lines.append("")

    best_candidate = summary[
        "best_entity_temporal_profile"
    ]

    if best_candidate is None:
        lines.append(
            "No entity-temporal candidate was detected."
        )
    else:
        for key, value in (
            best_candidate.items()
        ):
            lines.append(
                f"- **{key}:** {value}"
            )

    lines.append("")

    lines.append(
        "## Derived Analytical Target Risks"
    )
    lines.append("")

    risks = report[
        "derived_target_risks"
    ]

    if not risks:
        lines.append(
            "No derived analytical target risks "
            "were detected by configured heuristics."
        )
    else:
        for risk in risks:
            lines.append(
                f"- **{risk['severity']} — "
                f"{risk['column']}** in "
                f"`{risk['dataset_path']}`: "
                f"{risk['detail']}"
            )

    lines.append("")

    lines.append("## Domain Inventory")
    lines.append("")

    for domain, paths in (
        report[
            "domain_inventory"
        ].items()
    ):
        lines.append(
            f"### {domain}"
        )
        lines.append("")

        for path in paths:
            lines.append(
                f"- `{path}`"
            )

        lines.append("")

    lines.append(
        "## Dataset-Level Assessment"
    )
    lines.append("")

    lines.append(
        "| Dataset | Profile Mode | Rows Profiled "
        "| Temporal Columns | Primary Geography "
        "| Price Columns | Domains | Status |"
    )

    lines.append(
        "|---|---|---:|---|---|---|---|---|"
    )

    for dataset in report["datasets"]:
        lines.append(
            f"| {_markdown_escape(dataset['path'])} "
            f"| {_markdown_escape(dataset['profile_mode'])} "
            f"| {_markdown_escape(dataset['profiled_row_count'])} "
            f"| {_markdown_escape(_format_items(dataset['temporal_columns']))} "
            f"| {_markdown_escape(dataset['primary_geography_candidate'])} "
            f"| {_markdown_escape(_format_items(dataset['price_columns']))} "
            f"| {_markdown_escape(_format_items(dataset['detected_feature_domains']))} "
            f"| {_markdown_escape(dataset['profile_status'])} |"
        )

    lines.append("")

    lines.append(
        "## Architectural Interpretation"
    )
    lines.append("")

    lines.append(
        "This assessment measures structural predictive "
        "feasibility. It does not authorize model training."
    )

    lines.append("")

    lines.append(
        "A future prediction task still requires a formal "
        "prediction contract, target engineering policy, "
        "point-in-time feature policy, temporal split policy, "
        "and leakage validation."
    )

    lines.append("")

    output_path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def run_predictive_data_gap_assessment(
    project_root: Path,
    config_path: Path,
    readiness_report_path: Path,
    json_output_path: Path,
    markdown_output_path: Path,
) -> dict[str, Any]:
    report = (
        build_predictive_data_gap_report(
            project_root=project_root,
            config_path=config_path,
            readiness_report_path=(
                readiness_report_path
            ),
        )
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