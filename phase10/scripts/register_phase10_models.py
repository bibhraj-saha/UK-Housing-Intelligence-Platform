"""Register trained Phase 10 models."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

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

from uk_housing_ml.mlops.model_registry import (  # noqa: E402
    register_model,
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
            "Configuration must be "
            "a mapping."
        )

    return loaded


def _load_json(
    path: Path,
) -> dict[str, Any]:
    loaded = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    if not isinstance(
        loaded,
        dict,
    ):
        raise ValueError(
            "JSON report must be "
            "a mapping."
        )

    return loaded


def main() -> int:
    config_path = (
        PHASE10_ROOT
        / "config"
        / "mlops"
        / "model_registry.yaml"
    )

    config = _load_yaml(
        config_path
    )

    registry_config = config[
        "registry"
    ]

    registry_path = (
        PROJECT_ROOT
        / registry_config[
            "path"
        ]
    )

    default_stage = registry_config[
        "default_stage"
    ]

    registered_entries = []

    for task_name, task_config in (
        config[
            "tasks"
        ].items()
    ):
        if "evaluation_report" in (
            task_config
        ):
            report_path = (
                PROJECT_ROOT
                / task_config[
                    "evaluation_report"
                ]
            )

            report = _load_json(
                report_path
            )

            entry = register_model(
                registry_path=registry_path,
                task_name=task_name,
                model_name=report[
                    "best_model_name"
                ],
                artifact_path=report[
                    "model_path"
                ],
                metrics=report[
                    "test_metrics"
                ],
                stage=default_stage,
                metadata={
                    "selection_metric": (
                        report[
                            "selection_metric"
                        ]
                    ),
                    "source_report": str(
                        report_path.relative_to(
                            PROJECT_ROOT
                        )
                    ),
                },
            )

        else:
            report_path = (
                PROJECT_ROOT
                / task_config[
                    "forecasting_report"
                ]
            )

            report = _load_json(
                report_path
            )

            horizon = str(
                task_config[
                    "horizon"
                ]
            )

            horizon_result = (
                report[
                    "horizons"
                ][
                    horizon
                ]
            )

            if (
                horizon_result[
                    "status"
                ]
                != "trained"
            ):
                continue

            entry = register_model(
                registry_path=registry_path,
                task_name=task_name,
                model_name=horizon_result[
                    "best_model_name"
                ],
                artifact_path=horizon_result[
                    "model_path"
                ],
                metrics=horizon_result[
                    "test_metrics"
                ],
                stage=default_stage,
                metadata={
                    "horizon_months": int(
                        horizon
                    ),
                    "selection_metric": (
                        report[
                            "selection_metric"
                        ]
                    ),
                    "source_report": str(
                        report_path.relative_to(
                            PROJECT_ROOT
                        )
                    ),
                },
            )

        registered_entries.append(
            entry
        )

    print("=" * 72)
    print(
        "PHASE 10 MODEL REGISTRATION"
    )
    print("=" * 72)

    for entry in registered_entries:
        print(
            f"{entry.task_name}: "
            f"{entry.model_name} "
            f"v{entry.version} "
            f"[{entry.stage}]"
        )

    print("-" * 72)
    print(
        "Registered models:",
        len(
            registered_entries
        ),
    )
    print(
        "Registry:",
        registry_path,
    )
    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )