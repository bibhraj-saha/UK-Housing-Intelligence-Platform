"""Tests for model registry."""

import pytest

from uk_housing_ml.mlops.model_registry import (
    register_model,
)


def test_register_model_increments_version(
    tmp_path,
) -> None:
    registry_path = (
        tmp_path
        / "registry.json"
    )

    first = register_model(
        registry_path=registry_path,
        task_name="price_prediction",
        model_name="random_forest",
        artifact_path="model.joblib",
        metrics={
            "rmse": 10.0,
        },
    )

    second = register_model(
        registry_path=registry_path,
        task_name="price_prediction",
        model_name="random_forest",
        artifact_path="model.joblib",
        metrics={
            "rmse": 9.0,
        },
    )

    assert first.version == 1
    assert second.version == 2


def test_unknown_registry_stage_rejected(
    tmp_path,
) -> None:
    with pytest.raises(
        ValueError,
        match="Unknown model stage",
    ):
        register_model(
            registry_path=(
                tmp_path
                / "registry.json"
            ),
            task_name="price_prediction",
            model_name="random_forest",
            artifact_path="model.joblib",
            metrics={},
            stage="unknown",
        )