"""Tests for experiment tracking."""

from uk_housing_ml.mlops.experiment_tracker import (
    build_experiment_record,
    write_experiment_record,
)


def test_build_experiment_record() -> None:
    record = build_experiment_record(
        task_name="price_prediction",
        model_name="random_forest",
        metrics={
            "rmse": 10.0,
        },
    )

    assert (
        record.task_name
        == "price_prediction"
    )

    assert (
        record.model_name
        == "random_forest"
    )

    assert (
        record.metrics[
            "rmse"
        ]
        == 10.0
    )


def test_write_experiment_record(
    tmp_path,
) -> None:
    record = build_experiment_record(
        task_name="growth_prediction",
        model_name="ridge_regression",
    )

    output_path = (
        write_experiment_record(
            record=record,
            output_directory=tmp_path,
        )
    )

    assert output_path.is_file()