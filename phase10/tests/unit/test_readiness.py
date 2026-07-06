from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
PHASE10_SRC = PROJECT_ROOT / "phase10" / "src"

if str(PHASE10_SRC) not in sys.path:
    sys.path.insert(0, str(PHASE10_SRC))


from uk_housing_ml.audit.readiness import (
    DatasetProfile,
    build_readiness_summary,
    determine_overall_decision,
    discover_datasets,
)


def test_discover_datasets_finds_supported_files(
    tmp_path: Path,
) -> None:
    analytics_directory = tmp_path / "data" / "analytics"
    analytics_directory.mkdir(parents=True)

    parquet_path = analytics_directory / "sample.parquet"
    csv_path = analytics_directory / "sample.csv"
    ignored_path = analytics_directory / "notes.txt"

    pd.DataFrame(
        {
            "lsoa_code": ["E01000001"],
            "average_price": [250000.0],
        }
    ).to_parquet(
        parquet_path,
        index=False,
    )

    pd.DataFrame(
        {
            "lsoa_code": ["E01000001"],
            "average_price": [250000.0],
        }
    ).to_csv(
        csv_path,
        index=False,
    )

    ignored_path.write_text(
        "ignore me",
        encoding="utf-8",
    )

    config = {
        "discovery": {
            "supported_extensions": [
                ".parquet",
                ".csv",
            ],
            "recursive": True,
            "directories": [
                "data/analytics",
            ],
        }
    }

    discovered = discover_datasets(
        project_root=tmp_path,
        config=config,
    )

    discovered_names = {
        path.name
        for path in discovered
    }

    assert discovered_names == {
        "sample.parquet",
        "sample.csv",
    }


def test_build_readiness_summary_detects_core_signals() -> None:
    profile = DatasetProfile(
        path="data/analytics/example.parquet",
        file_name="example.parquet",
        extension=".parquet",
        file_size_bytes=100,
        row_count=10,
        column_count=4,
        columns=[
            "lsoa_code",
            "transaction_date",
            "average_price",
            "investment_score",
        ],
        dtypes={
            "lsoa_code": "object",
            "transaction_date": "datetime64[ns]",
            "average_price": "float64",
            "investment_score": "float64",
        },
        missingness_percent={
            "lsoa_code": 0.0,
            "transaction_date": 0.0,
            "average_price": 0.0,
            "investment_score": 0.0,
        },
        datetime_columns=[
            "transaction_date",
        ],
        datetime_ranges={
            "transaction_date": {
                "min": "2024-01-01T00:00:00",
                "max": "2024-12-31T00:00:00",
            }
        },
        geography_columns=[
            "lsoa_code",
        ],
        candidate_target_columns=[
            "average_price",
            "investment_score",
        ],
        leakage_risk_columns=[],
        derived_score_columns=[
            "investment_score",
        ],
        numeric_columns=[
            "average_price",
            "investment_score",
        ],
        categorical_columns=[
            "lsoa_code",
        ],
        duplicate_row_count=0,
        profile_status="success",
        profile_error=None,
    )

    summary = build_readiness_summary([profile])

    assert summary["dataset_count"] == 1
    assert summary["successful_dataset_count"] == 1
    assert summary["temporal_dataset_count"] == 1
    assert summary["geography_dataset_count"] == 1
    assert summary["price_signal_dataset_count"] == 1
    assert summary["investment_signal_dataset_count"] == 1


def test_overall_decision_is_no_go_without_datasets() -> None:
    summary = {
        "readiness_flags": {
            "has_datasets": False,
            "has_geography_signal": False,
            "has_temporal_signal": False,
        }
    }

    decision = determine_overall_decision(summary)

    assert decision == "NO_GO"


def test_overall_decision_is_no_go_without_geography() -> None:
    summary = {
        "readiness_flags": {
            "has_datasets": True,
            "has_geography_signal": False,
            "has_temporal_signal": True,
        }
    }

    decision = determine_overall_decision(summary)

    assert decision == "NO_GO"


def test_overall_decision_is_conditional_go_with_core_signals() -> None:
    summary = {
        "readiness_flags": {
            "has_datasets": True,
            "has_geography_signal": True,
            "has_temporal_signal": True,
        }
    }

    decision = determine_overall_decision(summary)

    assert decision == "CONDITIONAL_GO"