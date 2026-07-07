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

from uk_housing_ml.audit.data_gap import (

    run_predictive_data_gap_assessment,

)

def parse_arguments() -> argparse.Namespace:

    parser = argparse.ArgumentParser(

        description=(

            "Run the Phase 10 Predictive Data-Gap "

            "Assessment for the UK Housing "

            "Intelligence Platform."

        )

    )

    parser.add_argument(

        "--config",

        type=Path,

        default=(

            PROJECT_ROOT

            / "phase10"

            / "config"

            / "predictive_data_gap.yml"

        ),

        help=(

            "Path to the predictive data-gap "

            "configuration file."

        ),

    )

    parser.add_argument(

        "--readiness-report",

        type=Path,

        default=(

            PROJECT_ROOT

            / "phase10"

            / "reports"

            / "audits"

            / "ml_readiness_audit.json"

        ),

        help=(

            "Path to the Step 1 ML readiness "

            "JSON report."

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

            / "predictive_data_gap_assessment.json"

        ),

        help=(

            "Path for the machine-readable "

            "data-gap report."

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

            / "predictive_data_gap_assessment.md"

        ),

        help=(

            "Path for the human-readable "

            "data-gap report."

        ),

    )

    return parser.parse_args()

def _format_items(

    items: list[str],

) -> str:

    if not items:

        return "none"

    return ", ".join(items)

def print_horizon_feasibility(

    report: dict,

) -> None:

    print()

    print("CANDIDATE HORIZON FEASIBILITY")

    print("-" * 72)

    for horizon, assessment in (

        report[

            "horizon_feasibility"

        ].items()

    ):

        print(

            f"{horizon}: "

            f"{assessment['status']}"

        )

        print(

            f"  reason: "

            f"{assessment['reason']}"

        )

def print_task_assessments(

    report: dict,

) -> None:

    print()

    print("PREDICTIVE TASK GAP ASSESSMENT")

    print("-" * 72)

    for task_name, assessment in (

        report[

            "task_assessments"

        ].items()

    ):

        print(

            f"{task_name}: "

            f"{assessment['status']}"

        )

        print(

            "  missing required domains: "

            f"{_format_items(assessment['missing_required_domains'])}"

        )

        print(

            "  missing recommended domains: "

            f"{_format_items(assessment['missing_recommended_domains'])}"

        )

        print(

            "  required history months: "

            f"{assessment['required_history_months']}"

        )

        print(

            "  detected maximum history months: "

            f"{assessment['detected_maximum_history_months']}"

        )

        print(

            "  required median periods per entity: "

            f"{assessment['required_median_periods_per_entity']}"

        )

        gaps = assessment["gaps"]

        if not gaps:

            print(

                "  gaps: none detected"

            )

        else:

            print("  gaps:")

            for gap in gaps:

                print(

                    f"    - {gap['severity']} | "

                    f"{gap['gap_type']} | "

                    f"{gap['detail']}"

                )

        print()

def print_best_entity_temporal_candidate(

    report: dict,

) -> None:

    print()

    print("BEST ENTITY-TEMPORAL CANDIDATE")

    print("-" * 72)

    candidate = report[

        "summary"

    ][

        "best_entity_temporal_profile"

    ]

    if candidate is None:

        print(

            "No entity-temporal candidate detected."

        )

        return

    for key, value in candidate.items():

        print(

            f"{key}: {value}"

        )

def main() -> int:

    args = parse_arguments()

    report = (

        run_predictive_data_gap_assessment(

            project_root=PROJECT_ROOT,

            config_path=args.config,

            readiness_report_path=(

                args.readiness_report

            ),

            json_output_path=(

                args.json_output

            ),

            markdown_output_path=(

                args.markdown_output

            ),

        )

    )

    summary = report["summary"]

    print("=" * 72)

    print(

        "PHASE 10 PREDICTIVE DATA-GAP ASSESSMENT"

    )

    print("=" * 72)

    print(

        f"Overall decision: "

        f"{report['overall_decision']}"

    )

    print(

        f"Datasets assessed: "

        f"{summary['dataset_count']}"

    )

    print(

        "Successfully assessed: "

        f"{summary['successful_dataset_count']}"

    )

    print(

        f"Failed assessments: "

        f"{summary['failed_dataset_count']}"

    )

    print(

        "Available domains: "

        f"{_format_items(summary['available_domains'])}"

    )

    print(

        "Maximum detected history months: "

        f"{summary['maximum_detected_history_months']}"

    )

    print_horizon_feasibility(

        report

    )

    print_task_assessments(

        report

    )

    print_best_entity_temporal_candidate(

        report

    )

    print()

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