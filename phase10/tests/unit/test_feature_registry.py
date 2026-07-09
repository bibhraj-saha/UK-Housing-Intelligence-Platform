from __future__ import annotations

import pytest

from uk_housing_ml.features.registry import (
    build_feature_registry,
)


def test_registry_builds_enabled_features(
) -> None:
    config = {
        "feature_store": {
            "features": {
                "price_lag_1m": {
                    "enabled": True,
                    "source_role": "price",
                    "operation": "lag",
                    "periods": 1,
                },
                "disabled_feature": {
                    "enabled": False,
                    "source_role": "price",
                    "operation": "lag",
                    "periods": 2,
                },
            }
        }
    }

    registry = build_feature_registry(
        config
    )

    assert len(registry) == 1

    assert (
        registry[0].name
        == "price_lag_1m"
    )


def test_registry_requires_source_role(
) -> None:
    config = {
        "feature_store": {
            "features": {
                "bad_feature": {
                    "enabled": True,
                    "operation": "lag",
                    "periods": 1,
                }
            }
        }
    }

    with pytest.raises(
        ValueError,
        match="source_role",
    ):
        build_feature_registry(
            config
        )