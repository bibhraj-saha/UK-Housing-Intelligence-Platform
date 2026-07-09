from __future__ import annotations

import argparse
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


from uk_housing_ml.features.builder import (
    build_feature_store,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build the Phase 10 point-in-time "
            "feature store."
        )
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=(
            PROJECT_ROOT
            / "phase10"
            / "config"
            / "features"
            / "feature_store.yml"
        ),
    )

    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    result = build_feature_store(
        project_root=PROJECT_ROOT,
        config_path=args.config,
    )

    print("=" * 72)
    print("PHASE 10 FEATURE STORE BUILD")
    print("=" * 72)

    print(
        f"Rows: {result.row_count}"
    )

    print(
        f"Columns: {result.column_count}"
    )

    print(
        f"Entities: {result.entity_count}"
    )

    print(
        "Minimum timestamp: "
        f"{result.minimum_timestamp}"
    )

    print(
        "Maximum timestamp: "
        f"{result.maximum_timestamp}"
    )

    print(
        "Price source: "
        f"{result.source_price_column}"
    )

    print(
        "Transaction source: "
        f"{result.source_transaction_column}"
    )

    print(
        "Features: "
        + ", ".join(
            result.feature_columns
        )
    )

    print(
        f"Output: {result.output_path}"
    )

    print(
        f"Manifest: {result.manifest_path}"
    )

    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )