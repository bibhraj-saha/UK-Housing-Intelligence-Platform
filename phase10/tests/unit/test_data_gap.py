from __future__ import annotations

import pandas as pd

from uk_housing_ml.audit.data_gap import (
    _assess_horizon_feasibility,
    _assess_task_gaps,
    _build_entity_temporal_profile,
    _detect_feature_domains,
    _infer_frequency,
    _select_primary_geography_candidate,
)


def _build_gap_config() -> dict:
    return {
        "assessment": {
            "minimum_history_months": {
                "price_prediction": 24,
                "growth_prediction": 24,
                "forecasting": 36,
                "investment_opportunity_prediction": 24,
            },
            "minimum_periods_per_entity": {
                "price_prediction": 12,
                "growth_prediction": 12,
                "forecasting": 24,
                "investment_opportunity_prediction": 12,
            },
        },
        "geography_candidates": {
            "priority_order": [
                "lsoa_code",
                "lad_code",
                "region",
            ],
        },
    }


def test_select_primary_geography_prefers_lsoa(
) -> None:
    geography_columns = [
        "region",
        "lad_code",
        "lsoa_code",
    ]

    config = {
        "geography_candidates": {
            "priority_order": [
                "lsoa_code",
                "lad_code",
                "region",
            ],
        }
    }

    result = (
        _select_primary_geography_candidate(
            geography_columns=(
                geography_columns
            ),
            config=config,
        )
    )

    assert result == "lsoa_code"


def test_select_primary_geography_returns_none_without_geography(
) -> None:
    config = {
        "geography_candidates": {
            "priority_order": [
                "lsoa_code",
                "lad_code",
                "region",
            ],
        }
    }

    result = (
        _select_primary_geography_candidate(
            geography_columns=[],
            config=config,
        )
    )

    assert result is None


def test_infer_frequency_detects_monthly_series(
) -> None:
    series = pd.Series(
        pd.to_datetime(
            [
                "2025-01-01",
                "2025-02-01",
                "2025-03-01",
                "2025-04-01",
            ]
        )
    )

    frequency, median_gap_days = (
        _infer_frequency(
            series
        )
    )

    assert frequency == "monthly"
    assert median_gap_days is not None

    assert (
        28.0
        <= median_gap_days
        <= 31.0
    )


def test_infer_frequency_detects_daily_or_transactional_series(
) -> None:
    series = pd.Series(
        pd.to_datetime(
            [
                "2025-01-01",
                "2025-01-02",
                "2025-01-03",
                "2025-01-04",
            ]
        )
    )

    frequency, median_gap_days = (
        _infer_frequency(
            series
        )
    )

    assert (
        frequency
        == "daily_or_transactional"
    )

    assert median_gap_days == 1.0


def test_entity_temporal_profile_counts_monthly_periods(
) -> None:
    dataframe = pd.DataFrame(
        {
            "lsoa_code": [
                "A",
                "A",
                "A",
                "B",
                "B",
            ],
            "transfer_date": [
                "2025-01-10",
                "2025-02-10",
                "2025-02-20",
                "2025-01-15",
                "2025-03-15",
            ],
        }
    )

    parsed_series = pd.to_datetime(
        dataframe["transfer_date"],
        errors="coerce",
        utc=True,
    )

    profile = (
        _build_entity_temporal_profile(
            dataframe=dataframe,
            entity_column="lsoa_code",
            temporal_column="transfer_date",
            parsed_temporal_series=(
                parsed_series
            ),
        )
    )

    assert profile.unique_entity_count == 2

    assert (
        profile.entity_period_pair_count
        == 4
    )

    assert (
        profile.entities_with_multiple_periods
        == 2
    )

    assert profile.repeated_entity_ratio == 1.0

    assert (
        profile.minimum_periods_per_entity
        == 2
    )

    assert (
        profile.median_periods_per_entity
        == 2.0
    )

    assert (
        profile.maximum_periods_per_entity
        == 2
    )


def test_detect_feature_domains_from_columns(
) -> None:
    dataframe = pd.DataFrame(
        {
            "average_price": [100000.0],
            "crime_score": [0.7],
            "affordability_score": [0.8],
            "lsoa_code": ["A"],
        }
    )

    config = {
        "feature_domain_detection": {
            "price": {
                "tokens": [
                    "price",
                ],
            },
            "crime": {
                "tokens": [
                    "crime",
                ],
            },
            "affordability": {
                "tokens": [
                    "affordability",
                ],
            },
            "geography": {
                "tokens": [
                    "lsoa",
                ],
            },
            "investment": {
                "tokens": [
                    "investment",
                ],
            },
        }
    }

    detected = _detect_feature_domains(
        dataframe=dataframe,
        config=config,
    )

    assert detected == [
        "affordability",
        "crime",
        "geography",
        "price",
    ]


def test_three_month_horizon_is_structurally_feasible_with_long_history(
) -> None:
    result = (
        _assess_horizon_feasibility(
            maximum_history_months=12.0,
            horizons=[
                3,
            ],
        )
    )

    assert (
        result[
            "3_months"
        ]["status"]
        == "structurally_feasible"
    )


def test_twelve_month_horizon_is_weak_with_limited_history(
) -> None:
    result = (
        _assess_horizon_feasibility(
            maximum_history_months=18.0,
            horizons=[
                12,
            ],
        )
    )

    assert (
        result[
            "12_months"
        ]["status"]
        == "weakly_feasible"
    )


def test_twenty_four_month_horizon_is_not_feasible_with_short_history(
) -> None:
    result = (
        _assess_horizon_feasibility(
            maximum_history_months=12.0,
            horizons=[
                24,
            ],
        )
    )

    assert (
        result[
            "24_months"
        ]["status"]
        == "not_feasible"
    )


def test_horizon_is_not_evaluable_without_temporal_history(
) -> None:
    result = (
        _assess_horizon_feasibility(
            maximum_history_months=None,
            horizons=[
                12,
            ],
        )
    )

    assert (
        result[
            "12_months"
        ]["status"]
        == "not_evaluable"
    )


def test_task_is_blocked_when_required_domain_missing(
) -> None:
    task_config = {
        "required_domains": [
            "price",
            "temporal",
        ],
        "recommended_domains": [
            "crime",
        ],
        "target_requirement": {
            "target_type": "future_price",
            "requires_future_horizon": True,
        },
    }

    result = _assess_task_gaps(
        task_name="price_prediction",
        task_config=task_config,
        available_domains=[
            "price",
            "crime",
        ],
        maximum_history_months=36.0,
        best_entity_temporal_profile={
            "median_periods_per_entity": 24.0,
        },
        config=_build_gap_config(),
    )

    assert result["status"] == "blocked"

    assert (
        result[
            "missing_required_domains"
        ]
        == [
            "temporal",
        ]
    )

    assert any(
        gap["gap_type"]
        == "missing_required_domain"
        for gap in result["gaps"]
    )


def test_task_has_major_gaps_when_history_is_short(
) -> None:
    task_config = {
        "required_domains": [
            "price",
            "temporal",
        ],
        "recommended_domains": [],
        "target_requirement": {
            "target_type": "future_price",
            "requires_future_horizon": True,
        },
    }

    result = _assess_task_gaps(
        task_name="price_prediction",
        task_config=task_config,
        available_domains=[
            "price",
            "temporal",
        ],
        maximum_history_months=11.96,
        best_entity_temporal_profile={
            "median_periods_per_entity": 4.0,
        },
        config=_build_gap_config(),
    )

    assert result["status"] == "major_gaps"

    gap_types = {
        gap["gap_type"]
        for gap in result["gaps"]
    }

    assert "insufficient_history" in gap_types

    assert (
        "insufficient_repeated_entity_coverage"
        in gap_types
    )

    assert (
        "future_target_not_defined"
        in gap_types
    )


def test_task_requires_engineering_when_data_structure_is_sufficient(
) -> None:
    task_config = {
        "required_domains": [
            "price",
            "temporal",
        ],
        "recommended_domains": [
            "crime",
        ],
        "target_requirement": {
            "target_type": "future_price",
            "requires_future_horizon": True,
        },
    }

    result = _assess_task_gaps(
        task_name="price_prediction",
        task_config=task_config,
        available_domains=[
            "price",
            "temporal",
            "crime",
        ],
        maximum_history_months=48.0,
        best_entity_temporal_profile={
            "median_periods_per_entity": 24.0,
        },
        config=_build_gap_config(),
    )

    assert (
        result["status"]
        == "engineering_required"
    )

    assert (
        result[
            "missing_required_domains"
        ]
        == []
    )

    assert (
        result[
            "missing_recommended_domains"
        ]
        == []
    )

    assert any(
        gap["gap_type"]
        == "future_target_not_defined"
        for gap in result["gaps"]
    )