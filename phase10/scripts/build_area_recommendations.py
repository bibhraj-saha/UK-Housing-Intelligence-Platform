"""Build Phase 10 area recommendations."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


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

from uk_housing_ml.recommendation.area_ranker import (  # noqa: E402
    build_area_recommendations,
)


def _load_yaml(
    path: Path,
) -> dict[str, Any]:
    with path.open(
        "r",
        encoding="utf-8",
    ) as handle:
        loaded = yaml.safe_load(
            handle
        )

    if not isinstance(
        loaded,
        dict,
    ):
        raise ValueError(
            f"Configuration must be a mapping: {path}"
        )

    return loaded


def _resolve_project_path(
    value: str,
) -> Path:
    return (
        PROJECT_ROOT
        / value
    ).resolve()


def _normalise_timestamp_column(
    frame: pd.DataFrame,
    timestamp_column: str,
) -> pd.DataFrame:
    resolved_frame = frame.copy()

    if timestamp_column in resolved_frame.columns:
        resolved_frame[
            timestamp_column
        ] = pd.to_datetime(
            resolved_frame[
                timestamp_column
            ],
            errors="raise",
        )

        return resolved_frame

    if (
        resolved_frame.index.name
        == timestamp_column
    ):
        resolved_frame = (
            resolved_frame.reset_index()
        )

        resolved_frame[
            timestamp_column
        ] = pd.to_datetime(
            resolved_frame[
                timestamp_column
            ],
            errors="raise",
        )

        return resolved_frame

    timestamp_aliases = [
        "period_end",
        "month",
        "period",
        "snapshot_date",
        "transfer_date",
        "date",
    ]

    source_timestamp_column = next(
        (
            column
            for column in timestamp_aliases
            if column in resolved_frame.columns
        ),
        None,
    )

    if source_timestamp_column is None:
        raise ValueError(
            "Feature store does not contain "
            f"required timestamp column "
            f"'{timestamp_column}' or a "
            "supported temporal alias. "
            "Available columns: "
            f"{resolved_frame.columns.tolist()}"
        )

    resolved_frame = resolved_frame.rename(
        columns={
            source_timestamp_column: (
                timestamp_column
            ),
        }
    )

    resolved_frame[
        timestamp_column
    ] = pd.to_datetime(
        resolved_frame[
            timestamp_column
        ],
        errors="raise",
    )

    return resolved_frame


def main() -> int:
    config_path = (
        PHASE10_ROOT
        / "config"
        / "recommendation"
        / "area_recommendation.yaml"
    )

    feature_store_path = (
        PHASE10_ROOT
        / "data"
        / "feature_store"
        / "lsoa_monthly_features.parquet"
    )

    config = _load_yaml(
        config_path
    )

    frame = pd.read_parquet(
        feature_store_path
    )

    timestamp_column = str(
        config[
            "timestamp_column"
        ]
    )

    frame = _normalise_timestamp_column(
        frame=frame,
        timestamp_column=timestamp_column,
    )

    result = build_area_recommendations(
        frame=frame,
        config=config,
    )

    output_config = config[
        "output"
    ]

    output_path = _resolve_project_path(
        output_config[
            "parquet_path"
        ]
    )

    manifest_path = _resolve_project_path(
        output_config[
            "manifest_path"
        ]
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.recommendations.to_parquet(
        output_path,
        index=False,
    )

    manifest = {
        "generated_at_utc": (
            datetime.now(
                timezone.utc
            ).isoformat()
        ),
        "entity_column": config[
            "entity_column"
        ],
        "timestamp_column": (
            timestamp_column
        ),
        "row_count": int(
            len(
                result.recommendations
            )
        ),
        "feature_columns": (
            result.feature_columns
        ),
        "weights": result.weights,
        "output_path": str(
            output_path.relative_to(
                PROJECT_ROOT
            )
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
        "PHASE 10 AREA RECOMMENDATION BUILD"
    )
    print("=" * 72)
    print(
        "Rows:",
        len(
            result.recommendations
        ),
    )
    print(
        "Features:",
        ", ".join(
            result.feature_columns
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
        "TOP 10 AREAS"
    )
    print("-" * 72)
    print(
        result.recommendations.head(
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