from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[3]

PHASE10_SRC = (
    PROJECT_ROOT
    / "phase10"
    / "src"
)

if str(PHASE10_SRC) not in sys.path:
    sys.path.insert(
        0,
        str(PHASE10_SRC),
    )


from uk_housing_ml.audit.readiness import (
    DatasetProfile,
    build_observed_signals,
    build_readiness_summary,
    determine_overall_decision,
    discover_datasets,
    evaluate_task_requirements,
)


def make_profile(
    *,
    columns: list[str],
    datetime_columns: list[str] | None = None,
    geography_columns: list[str] | None = None,
    candidate_target_columns: list[str] | None = None,
    leakage_risk_columns: list[str] | None = None,
    derived_score_columns: list[str] | None = None,
    numeric_columns: list[str] | None = None,
) -> DatasetProfile:
    return DatasetProfile(
        path="data/analytics/example.parquet",
        file_name="example.parquet",
        extension=".parquet",
        file_size_bytes=100,
        row_count=10,
        column_count=len(columns),
        columns=columns,
        dtypes={
            column: "object"
            for column in columns
        },
        missingness_percent={
            column: 0.0
            for column in columns
        },
        datetime_columns=(
            datetime_columns or []
        ),
        datetime_ranges={},
        geography_columns=(
            geography_columns or []
        ),
        candidate_target_columns=(
            candidate_target_columns or []
        ),
        leakage_risk_columns=(
            leakage_risk_columns or []
        ),
        derived_score_columns=(
            derived_score_columns or []
        ),
        numeric_columns=(
            numeric_columns or []
        ),
        categorical_columns=[],
        duplicate_row_count=0,
        profile_status="success",
        profile_error=None,
    )


def make_config() -> dict:
    return {
        "signal_detection": {
            "price": {
                "column_name_tokens": [
                    "price",
                ],
            },
            "growth": {
                "column_name_tokens": [
                    "growth",
                ],
            },
            "investment": {
                "column_name_tokens": [
                    "investment",
                ],
            },
            "feature": {
                "minimum_numeric_feature_columns": 2,
            },
        },
        "readiness_rules": {
            "signal_to_flag_mapping": {
                "price_signal": "has_price_signal",
                "growth_signal": "has_growth_signal",
                "investment_signal": "has_investment_signal",
                "geography_signal": "has_geography_signal",
                "temporal_signal": "has_temporal_signal",
                "feature_signal": "has_feature_signal",
                "repeated_observations": (
                    "has_repeated_observation_signal"
                ),
            },
            "task_requirements": {
                "price_prediction": {
                    "required_signals": [
                        "price_signal",
                        "geography_signal",
                        "temporal_signal",
                    ],
                    "required_controls": [
                        "future_price_target_defined",
                    ],
                },
            },
        },
        "control_registry": {
            "future_price_target_defined": {
                "description": (
                    "A future price target is defined."
                ),
                "satisfied": False,
            },
        },
    }


def test_discover_datasets_finds_supported_files(
    tmp_path: Path,
) -> None:
    analytics_directory = (
        tmp_path
        / "data"
        / "analytics"
    )

    analytics_directory.mkdir(
        parents=True
    )

    parquet_path = (
        analytics_directory
        / "sample.parquet"
    )

    csv_path = (
        analytics_directory
        / "sample.csv"
    )

    ignored_path = (
        analytics_directory
        / "notes.txt"
    )

    dataframe = pd.DataFrame(
        {
            "lsoa_code": [
                "E01000001",
            ],
            "average_price": [
                250000.0,
            ],
        }
    )

    dataframe.to_parquet(
        parquet_path,
        index=False,
    )

    dataframe.to_csv(
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


def test_build_observed_signals_detects_core_signals() -> None:
    profile = make_profile(
        columns=[
            "lsoa_code",
            "transaction_date",
            "average_price",
            "growth_score",
            "investment_score",
            "crime_score",
        ],
        datetime_columns=[
            "transaction_date",
        ],
        geography_columns=[
            "lsoa_code",
        ],
        candidate_target_columns=[
            "average_price",
        ],
        derived_score_columns=[
            "growth_score",
            "investment_score",
            "crime_score",
        ],
        numeric_columns=[
            "average_price",
            "growth_score",
            "investment_score",
            "crime_score",
        ],
    )

    signals = build_observed_signals(
        profiles=[profile],
        config=make_config(),
    )

    assert signals["has_datasets"] is True
    assert signals["has_price_signal"] is True
    assert signals["has_growth_signal"] is True
    assert signals["has_investment_signal"] is True
    assert signals["has_geography_signal"] is True
    assert signals["has_temporal_signal"] is True
    assert signals["has_feature_signal"] is True

    assert (
        signals[
            "has_repeated_observation_signal"
        ]
        is True
    )


def test_task_is_not_ready_when_required_signal_missing() -> None:
    task_config = {
        "required_signals": [
            "price_signal",
            "geography_signal",
            "temporal_signal",
        ],
        "required_controls": [
            "future_price_target_defined",
        ],
    }

    observed_signals = {
        "has_price_signal": True,
        "has_geography_signal": True,
        "has_temporal_signal": False,
    }

    signal_mapping = {
        "price_signal": "has_price_signal",
        "geography_signal": "has_geography_signal",
        "temporal_signal": "has_temporal_signal",
    }

    control_registry = {
        "future_price_target_defined": {
            "description": (
                "A future price target is defined."
            ),
            "satisfied": False,
        },
    }

    assessment = evaluate_task_requirements(
        task_name="price_prediction",
        task_config=task_config,
        observed_signals=observed_signals,
        signal_to_flag_mapping=signal_mapping,
        control_registry=control_registry,
    )

    assert assessment["status"] == "not_ready"

    assert assessment["missing_signals"] == [
        "temporal_signal",
    ]


def test_task_is_conditional_go_when_signals_exist_but_control_missing() -> None:
    task_config = {
        "required_signals": [
            "price_signal",
            "geography_signal",
            "temporal_signal",
        ],
        "required_controls": [
            "future_price_target_defined",
        ],
    }

    observed_signals = {
        "has_price_signal": True,
        "has_geography_signal": True,
        "has_temporal_signal": True,
    }

    signal_mapping = {
        "price_signal": "has_price_signal",
        "geography_signal": "has_geography_signal",
        "temporal_signal": "has_temporal_signal",
    }

    control_registry = {
        "future_price_target_defined": {
            "description": (
                "A future price target is defined."
            ),
            "satisfied": False,
        },
    }

    assessment = evaluate_task_requirements(
        task_name="price_prediction",
        task_config=task_config,
        observed_signals=observed_signals,
        signal_to_flag_mapping=signal_mapping,
        control_registry=control_registry,
    )

    assert (
        assessment["status"]
        == "conditional_go"
    )

    assert assessment["missing_signals"] == []

    assert assessment["missing_controls"] == [
        "future_price_target_defined",
    ]


def test_task_is_go_when_signals_and_controls_exist() -> None:
    task_config = {
        "required_signals": [
            "price_signal",
            "geography_signal",
            "temporal_signal",
        ],
        "required_controls": [
            "future_price_target_defined",
        ],
    }

    observed_signals = {
        "has_price_signal": True,
        "has_geography_signal": True,
        "has_temporal_signal": True,
    }

    signal_mapping = {
        "price_signal": "has_price_signal",
        "geography_signal": "has_geography_signal",
        "temporal_signal": "has_temporal_signal",
    }

    control_registry = {
        "future_price_target_defined": {
            "description": (
                "A future price target is defined."
            ),
            "satisfied": True,
        },
    }

    assessment = evaluate_task_requirements(
        task_name="price_prediction",
        task_config=task_config,
        observed_signals=observed_signals,
        signal_to_flag_mapping=signal_mapping,
        control_registry=control_registry,
    )

    assert assessment["status"] == "go"
    assert assessment["missing_signals"] == []
    assert assessment["missing_controls"] == []

    assert assessment["met_controls"] == [
        "future_price_target_defined",
    ]


def test_unknown_signal_mapping_raises_error() -> None:
    task_config = {
        "required_signals": [
            "unknown_signal",
        ],
        "required_controls": [],
    }

    with pytest.raises(
        ValueError,
        match="No readiness flag mapping exists",
    ):
        evaluate_task_requirements(
            task_name="example_task",
            task_config=task_config,
            observed_signals={},
            signal_to_flag_mapping={},
            control_registry={},
        )


def test_unknown_control_raises_error() -> None:
    task_config = {
        "required_signals": [],
        "required_controls": [
            "unknown_control",
        ],
    }

    with pytest.raises(
        ValueError,
        match="No control registry entry exists",
    ):
        evaluate_task_requirements(
            task_name="example_task",
            task_config=task_config,
            observed_signals={},
            signal_to_flag_mapping={},
            control_registry={},
        )


def test_build_readiness_summary_uses_configuration() -> None:
    profile = make_profile(
        columns=[
            "lsoa_code",
            "transaction_date",
            "average_price",
            "crime_score",
        ],
        datetime_columns=[
            "transaction_date",
        ],
        geography_columns=[
            "lsoa_code",
        ],
        candidate_target_columns=[
            "average_price",
        ],
        derived_score_columns=[
            "crime_score",
        ],
        numeric_columns=[
            "average_price",
            "crime_score",
        ],
    )

    summary = build_readiness_summary(
        profiles=[profile],
        config=make_config(),
    )

    assessment = summary[
        "task_assessment"
    ][
        "price_prediction"
    ]

    assert (
        assessment["status"]
        == "conditional_go"
    )

    assert assessment["met_signals"] == [
        "price_signal",
        "geography_signal",
        "temporal_signal",
    ]

    assert assessment["missing_signals"] == []

    assert assessment["missing_controls"] == [
        "future_price_target_defined",
    ]


def test_overall_decision_is_no_go_when_all_tasks_not_ready() -> None:
    summary = {
        "task_assessment": {
            "price_prediction": {
                "status": "not_ready",
            },
            "growth_prediction": {
                "status": "not_ready",
            },
        }
    }

    decision = determine_overall_decision(
        summary
    )

    assert decision == "NO_GO"


def test_overall_decision_is_conditional_go_when_any_task_is_conditional() -> None:
    summary = {
        "task_assessment": {
            "price_prediction": {
                "status": "conditional_go",
            },
            "growth_prediction": {
                "status": "not_ready",
            },
        }
    }

    decision = determine_overall_decision(
        summary
    )

    assert decision == "CONDITIONAL_GO"


def test_overall_decision_is_go_when_all_tasks_are_go() -> None:
    summary = {
        "task_assessment": {
            "price_prediction": {
                "status": "go",
            },
            "growth_prediction": {
                "status": "go",
            },
        }
    }

    decision = determine_overall_decision(
        summary
    )

    assert decision == "GO"