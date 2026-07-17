"""Validate final Phase 10 integration."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

PHASE10_ROOT = (
    PROJECT_ROOT
    / "phase10"
)


def _require_file(
    path: Path,
) -> None:
    if not path.is_file():
        raise RuntimeError(
            f"Required file missing: {path}"
        )


def main() -> int:
    required_files = [
        PHASE10_ROOT
        / "artifacts"
        / "models"
        / "price_prediction"
        / "best_model.joblib",

        PHASE10_ROOT
        / "artifacts"
        / "models"
        / "growth_prediction"
        / "best_model.joblib",

        PHASE10_ROOT
        / "artifacts"
        / "models"
        / "investment_opportunity_prediction"
        / "best_model.joblib",

        PHASE10_ROOT
        / "artifacts"
        / "registry"
        / "model_registry.json",

        PHASE10_ROOT
        / "reports"
        / "monitoring"
        / "feature_drift_report.json",

        PHASE10_ROOT
        / "data"
        / "recommendations"
        / "area_recommendation"
        / "area_recommendations.parquet",

        PHASE10_ROOT
        / "data"
        / "serving"
        / "area_ml_serving.parquet",

        PHASE10_ROOT
        / "reports"
        / "forecasting"
        / "forecasting_evaluation_report.json",
    ]

    for horizon in [
        3,
        6,
        12,
        24,
    ]:
        required_files.append(
            PHASE10_ROOT
            / "artifacts"
            / "models"
            / "forecasting"
            / f"{horizon}_months"
            / "best_model.joblib"
        )

    for path in required_files:
        _require_file(
            path
        )

    registry_path = (
        PHASE10_ROOT
        / "artifacts"
        / "registry"
        / "model_registry.json"
    )

    registry = json.loads(
        registry_path.read_text(
            encoding="utf-8"
        )
    )

    expected_registry_tasks = {
        "price_prediction",
        "growth_prediction",
        "investment_opportunity_prediction",
        "forecasting_3_months",
        "forecasting_6_months",
        "forecasting_12_months",
        "forecasting_24_months",
    }

    actual_registry_tasks = set(
        registry[
            "models"
        ]
    )

    missing_registry_tasks = (
        expected_registry_tasks
        - actual_registry_tasks
    )

    if missing_registry_tasks:
        raise RuntimeError(
            "Missing registered tasks: "
            f"{sorted(missing_registry_tasks)}"
        )

    serving_path = (
        PHASE10_ROOT
        / "data"
        / "serving"
        / "area_ml_serving.parquet"
    )

    serving = pd.read_parquet(
        serving_path
    )

    required_serving_columns = {
        "lsoa_code",
        "recommendation_rank",
        "recommendation_score",
        "opportunity_probability",
        "predicted_future_price",
        "predicted_future_growth",
    }

    missing_serving_columns = (
        required_serving_columns
        - set(
            serving.columns
        )
    )

    if missing_serving_columns:
        raise RuntimeError(
            "Missing serving columns: "
            f"{sorted(missing_serving_columns)}"
        )

    if serving.empty:
        raise RuntimeError(
            "ML serving dataset is empty."
        )

    monitoring_path = (
        PHASE10_ROOT
        / "reports"
        / "monitoring"
        / "feature_drift_report.json"
    )

    monitoring = json.loads(
        monitoring_path.read_text(
            encoding="utf-8"
        )
    )

    print("=" * 72)
    print(
        "PHASE 10 FINAL INTEGRATION VALIDATION"
    )
    print("=" * 72)
    print(
        "Required files:",
        len(
            required_files
        ),
    )
    print(
        "Registered tasks:",
        len(
            actual_registry_tasks
        ),
    )
    print(
        "Serving rows:",
        len(
            serving
        ),
    )
    print(
        "Serving columns:",
        len(
            serving.columns
        ),
    )
    print(
        "Monitoring status:",
        monitoring[
            "overall_status"
        ],
    )
    print("-" * 72)
    print(
        "PHASE 10 INTEGRATION VALIDATION: PASSED"
    )
    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )