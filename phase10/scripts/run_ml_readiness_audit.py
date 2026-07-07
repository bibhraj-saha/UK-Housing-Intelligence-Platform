from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

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
    run_readiness_audit,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the Phase 10 ML readiness audit for the "
            "UK Housing Intelligence Platform."
        )
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=(
            PROJECT_ROOT
            / "phase10"
            / "config"
            / "readiness_audit.yml"
        ),
        help=(
            "Path to the readiness audit YAML "
            "configuration."
        ),
    )

    parser.add_argument(
        "--json-output",
        type=Path,
        default=(
            PROJECT_ROOT
            / "phase10"
            / "reports"
            / "audits"
            / "ml_readiness_audit.json"
        ),
        help=(
            "Path for the machine-readable JSON "
            "audit report."
        ),
    )

    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=(
            PROJECT_ROOT
            / "phase10"
            / "reports"
            / "audits"
            / "ml_readiness_audit.md"
        ),
        help=(
            "Path for the human-readable Markdown "
            "audit report."
        ),
    )

    return parser.parse_args()


def _format_items(
    items: list[str],
) -> str:
    if not items:
        return "none"

    return ", ".join(items)


def print_task_assessments(
    report: dict,
) -> None:
    task_assessments = report[
        "task_assessments"
    ]

    print()
    print("TASK READINESS")
    print("-" * 72)

    for task_name, assessment in (
        task_assessments.items()
    ):
        print(
            f"{task_name}: "
            f"{assessment['status']}"
        )

        print(
            "  met signals: "
            f"{_format_items(assessment['met_signals'])}"
        )

        print(
            "  missing signals: "
            f"{_format_items(assessment['missing_signals'])}"
        )

        print(
            "  met controls: "
            f"{_format_items(assessment['met_controls'])}"
        )

        print(
            "  missing controls: "
            f"{_format_items(assessment['missing_controls'])}"
        )

        print(
            "  reason: "
            f"{assessment['reason']}"
        )

        print()


def main() -> int:
    args = parse_arguments()

    report = run_readiness_audit(
        project_root=PROJECT_ROOT,
        config_path=args.config,
        json_output_path=args.json_output,
        markdown_output_path=(
            args.markdown_output
        ),
    )

    summary = report["summary"]

    print("=" * 72)
    print("PHASE 10 ML READINESS AUDIT")
    print("=" * 72)

    print(
        f"Overall decision: "
        f"{report['overall_decision']}"
    )

    print(
        f"Datasets discovered: "
        f"{summary['dataset_count']}"
    )

    print(
        "Successfully profiled: "
        f"{summary['successful_dataset_count']}"
    )

    print(
        f"Failed profiles: "
        f"{summary['failed_dataset_count']}"
    )

    print(
        "Temporal datasets: "
        f"{summary['temporal_dataset_count']}"
    )

    print(
        "Geography datasets: "
        f"{summary['geography_dataset_count']}"
    )

    print(
        "Candidate-target datasets: "
        f"{summary['candidate_target_dataset_count']}"
    )

    print(
        "Leakage-review datasets: "
        f"{summary['leakage_review_dataset_count']}"
    )

    print_task_assessments(report)

    print("-" * 72)

    print(
        f"JSON report: "
        f"{args.json_output}"
    )

    print(
        f"Markdown report: "
        f"{args.markdown_output}"
    )

    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())