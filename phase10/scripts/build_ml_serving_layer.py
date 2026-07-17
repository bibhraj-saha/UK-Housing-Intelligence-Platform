"""Build final Phase 10 ML serving layer."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

PHASE10_ROOT = (
    PROJECT_ROOT
    / "phase10"
)

SRC_ROOT = (
    PHASE10_ROOT
    / "src"
)

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(SRC_ROOT),
    )

from uk_housing_ml.integration.serving_builder import (  # noqa: E402
    build_area_ml_serving_dataset,
)


def main() -> int:
    recommendation_path = (
        PHASE10_ROOT
        / "data"
        / "recommendations"
        / "area_recommendation"
        / "area_recommendations.parquet"
    )

    investment_path = (
        PHASE10_ROOT
        / "data"
        / "predictions"
        / "investment_opportunity_prediction"
        / "test_predictions.parquet"
    )

    price_path = (
        PHASE10_ROOT
        / "data"
        / "predictions"
        / "price_prediction"
        / "test_predictions.parquet"
    )

    growth_path = (
        PHASE10_ROOT
        / "data"
        / "predictions"
        / "growth_prediction"
        / "test_predictions.parquet"
    )

    output_path = (
        PHASE10_ROOT
        / "data"
        / "serving"
        / "area_ml_serving.parquet"
    )

    manifest_path = (
        PHASE10_ROOT
        / "data"
        / "serving"
        / "area_ml_serving_manifest.json"
    )

    recommendations = (
        pd.read_parquet(
            recommendation_path
        )
    )

    investment_predictions = (
        pd.read_parquet(
            investment_path
        )
    )

    price_predictions = (
        pd.read_parquet(
            price_path
        )
    )

    growth_predictions = (
        pd.read_parquet(
            growth_path
        )
    )

    serving = (
        build_area_ml_serving_dataset(
            recommendations=(
                recommendations
            ),
            investment_predictions=(
                investment_predictions
            ),
            price_predictions=(
                price_predictions
            ),
            growth_predictions=(
                growth_predictions
            ),
        )
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    serving.to_parquet(
        output_path,
        index=False,
    )

    manifest = {
        "generated_at_utc": (
            datetime.now(
                timezone.utc
            ).isoformat()
        ),
        "row_count": int(
            len(
                serving
            )
        ),
        "column_count": int(
            len(
                serving.columns
            )
        ),
        "columns": (
            serving.columns.tolist()
        ),
        "output_path": str(
            output_path.relative_to(
                PROJECT_ROOT
            )
        ),
        "purpose": (
            "Dashboard-ready Phase 10 "
            "ML serving dataset"
        ),
    }

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("=" * 72)
    print(
        "PHASE 10 ML SERVING LAYER"
    )
    print("=" * 72)
    print(
        "Rows:",
        len(
            serving
        ),
    )
    print(
        "Columns:",
        len(
            serving.columns
        ),
    )
    print(
        "Output:",
        output_path,
    )
    print(
        "Manifest:",
        manifest_path,
    )
    print("-" * 72)
    print(
        serving.head(
            10
        ).to_string(
            index=False
        )
    )
    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )