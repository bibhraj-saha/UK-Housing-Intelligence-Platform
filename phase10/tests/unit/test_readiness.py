from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

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
    build_observed_signals,
    build_readiness_summary,
    determine_overall_decision,
    evaluate_task_requirements,
)


def _build_profile(
    *,
    columns: list[str] | None = None,
    datetime_columns: list[str] | None = None,
    geography_columns: list[str] | None = None,
    candidate_target_columns: list[str] | None = None,
    derived_score_columns: list[str] | None = None,
    numeric_columns: list[str] | None = None,
    profile_status: str = "success",
) -> SimpleNamespace:
    return SimpleNamespace(
        columns=(
            columns
            if columns is not None
            else []
        ),
        datetime_columns=(
            datetime_columns
            if datetime_columns is not None
            else []
        ),
        geography_columns=(
            geography_columns
            if geography_columns is not None
            else []
        ),
        candidate_target_columns=(
            candidate_target_columns
            if candidate_target_columns is not None
            else []
        ),
        derived_score_columns=(
            derived_score_columns
            if derived_score_columns is not None
            else []
        ),
        numeric_columns=(
            numeric_columns
            if numeric_columns is not None
            else []
        ),
        profile_status=profile_status,
    )


def _build_signal_config() -> dict:
    return {
        "signal_detection": {
            "price_signal": {
                "column_tokens": [
                    "price",
                ],
            },
            "growth_signal": {
                "column_tokens": [
                    "growth",
                ],
            },
            "investment_signal": {
                "column_tokens": [
                    "investment",
                ],
            },
        }
    }


def test_build_observed_signals_detects_core_signals(
) -> None:
    profiles = [
        _build_profile(
            columns=[
                "lsoa_code",
                "transfer_date",
                "average_price",
                "price_growth",
                "investment_score",
            ],
            datetime_columns=[
                "transfer_date",
            ],
            geography_columns=[
                "lsoa_code",
            ],
            candidate_target_columns=[
                "average_price",
            ],
            derived_score_columns=[
                "investment_score",
            ],
            numeric_columns=[
                "average_price",
                "price_growth",
                "investment_score",
            ],
        )
    ]

    observed = build_observed_signals(
        profiles=profiles,
        config=_build_signal_config(),
    )

    assert observed[
        "has_datasets"
    ] is True

    assert observed[
        "has_price_signal"
    ] is True

    assert observed[
        "has_growth_signal"
    ] is True

    assert observed[
        "has_investment_signal"
    ] is True

    assert observed[
        "has_geography_signal"
    ] is True

    assert observed[
        "has_temporal_signal"
    ] is True

    assert observed[
        "has_feature_signal"
    ] is True

    assert observed[
        "has_repeated_observation_signal"
    ] is True


def test_build_observed_signals_ignores_failed_profiles(
) -> None:
    profiles = [
        _build_profile(
            columns=[
                "average_price",
            ],
            candidate_target_columns=[
                "average_price",
            ],
            numeric_columns=[
                "average_price",
            ],
            profile_status="failed",
        )
    ]

    observed = build_observed_signals(
        profiles=profiles,
        config=_build_signal_config(),
    )

    assert observed[
        "has_datasets"
    ] is False

    assert observed[
        "has_price_signal"
    ] is False

    assert observed[
        "has_feature_signal"
    ] is False


def test_task_is_not_ready_when_required_signal_missing(
) -> None:
    result = evaluate_task_requirements(
        task_name="price_prediction",
        task_config={
            "required_signals": [
                "price",
                "temporal",
            ],
            "required_controls": [],
        },
        observed_signals={
            "has_price_signal": True,
            "has_temporal_signal": False,
        },
        signal_to_flag_mapping={
            "price": "has_price_signal",
            "temporal": "has_temporal_signal",
        },
        control_registry={},
    )

    assert result[
        "status"
    ] == "not_ready"

    assert result[
        "met_signals"
    ] == [
        "price",
    ]

    assert result[
        "missing_signals"
    ] == [
        "temporal",
    ]


def test_task_is_go_when_required_signals_exist(
) -> None:
    result = evaluate_task_requirements(
        task_name="price_prediction",
        task_config={
            "required_signals": [
                "price",
                "temporal",
            ],
            "required_controls": [],
        },
        observed_signals={
            "has_price_signal": True,
            "has_temporal_signal": True,
        },
        signal_to_flag_mapping={
            "price": "has_price_signal",
            "temporal": "has_temporal_signal",
        },
        control_registry={},
    )

    assert result[
        "status"
    ] == "go"

    assert result[
        "missing_signals"
    ] == []

    assert result[
        "missing_controls"
    ] == []


def test_unknown_signal_mapping_raises_error(
) -> None:
    with pytest.raises(
        KeyError,
        match="unknown_signal",
    ):
        evaluate_task_requirements(
            task_name="price_prediction",
            task_config={
                "required_signals": [
                    "unknown_signal",
                ],
                "required_controls": [],
            },
            observed_signals={
                "has_price_signal": True,
            },
            signal_to_flag_mapping={
                "price": "has_price_signal",
            },
            control_registry={},
        )


def test_unknown_control_raises_error(
) -> None:
    with pytest.raises(
        KeyError,
        match="unknown_control",
    ):
        evaluate_task_requirements(
            task_name="price_prediction",
            task_config={
                "required_signals": [
                    "price",
                ],
                "required_controls": [
                    "unknown_control",
                ],
            },
            observed_signals={
                "has_price_signal": True,
            },
            signal_to_flag_mapping={
                "price": "has_price_signal",
            },
            control_registry={},
        )


def test_build_readiness_summary_uses_configuration(
) -> None:
    profiles = [
        _build_profile(
            columns=[
                "lsoa_code",
                "transfer_date",
                "average_price",
            ],
            datetime_columns=[
                "transfer_date",
            ],
            geography_columns=[
                "lsoa_code",
            ],
            candidate_target_columns=[
                "average_price",
            ],
            numeric_columns=[
                "average_price",
            ],
        )
    ]

    config = {
        **_build_signal_config(),
        "readiness": {
            "signal_to_flag_mapping": {
                "price": (
                    "has_price_signal"
                ),
                "temporal": (
                    "has_temporal_signal"
                ),
            },
            "control_registry": {},
            "task_requirements": {
                "price_prediction": {
                    "required_signals": [
                        "price",
                        "temporal",
                    ],
                    "required_controls": [],
                },
            },
        },
    }

    summary = build_readiness_summary(
        profiles=profiles,
        config=config,
    )

    assert (
        summary[
            "observed_signals"
        ][
            "has_price_signal"
        ]
        is True
    )

    assert (
        summary[
            "observed_signals"
        ][
            "has_temporal_signal"
        ]
        is True
    )

    assert (
        summary[
            "task_assessments"
        ][
            "price_prediction"
        ][
            "status"
        ]
        == "go"
    )


def test_build_readiness_summary_marks_missing_signal_not_ready(
) -> None:
    profiles = [
        _build_profile(
            columns=[
                "average_price",
            ],
            candidate_target_columns=[
                "average_price",
            ],
            numeric_columns=[
                "average_price",
            ],
        )
    ]

    config = {
        **_build_signal_config(),
        "readiness": {
            "signal_to_flag_mapping": {
                "price": (
                    "has_price_signal"
                ),
                "temporal": (
                    "has_temporal_signal"
                ),
            },
            "control_registry": {},
            "task_requirements": {
                "price_prediction": {
                    "required_signals": [
                        "price",
                        "temporal",
                    ],
                    "required_controls": [],
                },
            },
        },
    }

    summary = build_readiness_summary(
        profiles=profiles,
        config=config,
    )

    assessment = summary[
        "task_assessments"
    ][
        "price_prediction"
    ]

    assert assessment[
        "status"
    ] == "not_ready"

    assert assessment[
        "missing_signals"
    ] == [
        "temporal",
    ]


def test_overall_decision_is_no_go_when_all_tasks_not_ready(
) -> None:
    task_assessments = {
        "price_prediction": {
            "status": "not_ready",
        },
        "growth_prediction": {
            "status": "not_ready",
        },
    }

    decision = determine_overall_decision(
        task_assessments
    )

    assert decision == "NO_GO"


def test_overall_decision_is_conditional_go_when_any_task_is_conditional(
) -> None:
    task_assessments = {
        "price_prediction": {
            "status": "go",
        },
        "growth_prediction": {
            "status": "conditional_go",
        },
    }

    decision = determine_overall_decision(
        task_assessments
    )

    assert decision == "CONDITIONAL_GO"


def test_overall_decision_is_go_when_all_tasks_are_go(
) -> None:
    task_assessments = {
        "price_prediction": {
            "status": "go",
        },
        "growth_prediction": {
            "status": "go",
        },
    }

    decision = determine_overall_decision(
        task_assessments
    )

    assert decision == "GO"