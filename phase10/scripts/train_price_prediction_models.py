"""Train Phase 10 price prediction models."""

from __future__ import annotations

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


from uk_housing_ml.training.experiment_runner import (  # noqa: E402
    run_regression_experiment,
)


def main() -> int:
    config_path = (
        PROJECT_ROOT
        / "phase10"
        / "configs"
        / "models"
        / "price_prediction.yaml"
    )

    report = run_regression_experiment(
        project_root=PROJECT_ROOT,
        config_path=config_path,
    )

    print("=" * 72)
    print(
        "PHASE 10 PRICE PREDICTION"
    )
    print("=" * 72)

    print(
        "Best model:",
        report["best_model_name"],
    )

    print(
        "Selection metric:",
        report["selection_metric"],
    )

    print("\nVALIDATION RESULTS")
    print("-" * 72)

    for model_name, result in (
        report[
            "validation_results"
        ].items()
    ):
        metrics = result["metrics"]

        print(
            f"{model_name}: "
            f"MAE={metrics['mae']:.6f}, "
            f"RMSE={metrics['rmse']:.6f}, "
            f"R2={metrics['r2']:.6f}"
        )

    print("\nFINAL TEST RESULTS")
    print("-" * 72)

    test_metrics = report[
        "test_metrics"
    ]

    print(
        f"MAE={test_metrics['mae']:.6f}"
    )

    print(
        f"RMSE={test_metrics['rmse']:.6f}"
    )

    print(
        f"R2={test_metrics['r2']:.6f}"
    )

    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )