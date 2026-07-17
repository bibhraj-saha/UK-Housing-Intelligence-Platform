"""Run Phase 10 feature drift monitoring."""

from __future__ import annotations

import json
import sys
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

from uk_housing_ml.monitoring.model_monitor import (  # noqa: E402
    build_monitoring_report,
)


def _load_yaml(
    path: Path,
) -> dict[str, Any]:
    loaded = yaml.safe_load(
        path.read_text(
            encoding="utf-8"
        )
    )

    if not isinstance(
        loaded,
        dict,
    ):
        raise ValueError(
            "Monitoring configuration "
            "must be a mapping."
        )

    return loaded


def main() -> int:
    config_path = (
        PHASE10_ROOT
        / "config"
        / "monitoring"
        / "monitoring.yaml"
    )

    config = _load_yaml(
        config_path
    )

    reference_path = (
        PROJECT_ROOT
        / config[
            "datasets"
        ][
            "reference"
        ]
    )

    current_path = (
        PROJECT_ROOT
        / config[
            "datasets"
        ][
            "current"
        ]
    )

    output_path = (
        PROJECT_ROOT
        / config[
            "output"
        ][
            "report"
        ]
    )

    reference_frame = (
        pd.read_parquet(
            reference_path
        )
    )

    current_frame = (
        pd.read_parquet(
            current_path
        )
    )

    monitoring_config = config[
        "monitoring"
    ]

    report = build_monitoring_report(
        task_name="phase10_feature_monitoring",
        reference_frame=reference_frame,
        current_frame=current_frame,
        feature_columns=monitoring_config[
            "feature_columns"
        ],
        drift_threshold=float(
            monitoring_config[
                "drift_threshold"
            ]
        ),
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("=" * 72)
    print(
        "PHASE 10 MODEL MONITORING"
    )
    print("=" * 72)
    print(
        "Status:",
        report[
            "overall_status"
        ],
    )
    print(
        "Reference rows:",
        report[
            "reference_rows"
        ],
    )
    print(
        "Current rows:",
        report[
            "current_rows"
        ],
    )
    print(
        "Monitored features:",
        report[
            "monitored_feature_count"
        ],
    )
    print(
        "Drifted features:",
        report[
            "drifted_feature_count"
        ],
    )

    if report[
        "drifted_features"
    ]:
        print(
            "Detected:",
            ", ".join(
                report[
                    "drifted_features"
                ]
            ),
        )

    print(
        "Report:",
        output_path,
    )
    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )