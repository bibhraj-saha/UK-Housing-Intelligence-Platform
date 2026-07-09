from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

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


from uk_housing_ml.training.dataset_builder import (
    build_training_dataset,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build Phase 10 point-in-time "
            "training datasets."
        )
    )

    parser.add_argument(
        "--feature-store",
        type=Path,
        default=(
            PROJECT_ROOT
            / "phase10"
            / "data"
            / "feature_store"
            / "lsoa_monthly_features.parquet"
        ),
    )

    parser.add_argument(
        "--feature-manifest",
        type=Path,
        default=(
            PROJECT_ROOT
            / "phase10"
            / "data"
            / "feature_store"
            / "lsoa_monthly_features_manifest.json"
        ),
    )

    parser.add_argument(
        "--contracts",
        type=Path,
        nargs="+",
        default=[
            (
                PROJECT_ROOT
                / "phase10"
                / "config"
                / "contracts"
                / "price_prediction.yml"
            ),
            (
                PROJECT_ROOT
                / "phase10"
                / "config"
                / "contracts"
                / "growth_prediction.yml"
            ),
        ],
    )

    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    manifest = json.loads(
        args.feature_manifest.read_text(
            encoding="utf-8"
        )
    )

    source_price_column = str(
        manifest[
            "result"
        ][
            "source_price_column"
        ]
    )

    print("=" * 72)
    print("PHASE 10 TRAINING DATASET BUILD")
    print("=" * 72)

    for contract_path in args.contracts:
        result = build_training_dataset(
            project_root=PROJECT_ROOT,
            feature_store_path=(
                args.feature_store
            ),
            contract_path=contract_path,
            source_price_column=(
                source_price_column
            ),
        )

        print(
            f"Task: {result.task_name}"
        )

        print(
            f"Target: {result.target_column}"
        )

        print(
            f"Total rows: {result.total_rows}"
        )

        print(
            f"Train rows: {result.train_rows}"
        )

        print(
            "Validation rows: "
            f"{result.validation_rows}"
        )

        print(
            f"Test rows: {result.test_rows}"
        )

        print(
            "Train end: "
            f"{result.train_end_timestamp}"
        )

        print(
            "Validation end: "
            f"{result.validation_end_timestamp}"
        )

        print(
            "Features: "
            + ", ".join(
                result.feature_columns
            )
        )

        print(
            "Rejected leakage columns: "
            + (
                ", ".join(
                    result.rejected_leakage_columns
                )
                if (
                    result.rejected_leakage_columns
                )
                else "none"
            )
        )

        print(
            "Output directory: "
            f"{result.output_directory}"
        )

        print("-" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )