"""Tests for area recommendation ranking."""

import pandas as pd
import pytest

from uk_housing_ml.recommendation.area_ranker import (
    build_area_recommendations,
)


def test_area_ranker_uses_latest_snapshot() -> None:
    frame = pd.DataFrame(
        {
            "lsoa_code": [
                "A",
                "A",
                "B",
                "B",
            ],
            "timestamp": pd.to_datetime(
                [
                    "2025-01-31",
                    "2025-02-28",
                    "2025-01-31",
                    "2025-02-28",
                ]
            ),
            "price_growth_3m": [
                0.01,
                0.10,
                0.02,
                0.05,
            ],
            "transaction_count": [
                5,
                20,
                10,
                15,
            ],
        }
    )

    result = build_area_recommendations(
        frame,
        config={
            "entity_column": "lsoa_code",
            "timestamp_column": "timestamp",
            "features": {
                "price_growth_3m": {
                    "weight": 0.5,
                    "higher_is_better": True,
                },
                "transaction_count": {
                    "weight": 0.5,
                    "higher_is_better": True,
                },
            },
        },
    )

    assert len(
        result.recommendations
    ) == 2

    assert (
        result.recommendations.iloc[
            0
        ]["lsoa_code"]
        == "A"
    )


def test_area_ranker_rejects_invalid_weights() -> None:
    frame = pd.DataFrame(
        {
            "lsoa_code": [
                "A",
            ],
            "timestamp": pd.to_datetime(
                [
                    "2025-01-31",
                ]
            ),
            "price_growth_3m": [
                0.1,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="sum to 1.0",
    ):
        build_area_recommendations(
            frame,
            config={
                "features": {
                    "price_growth_3m": {
                        "weight": 0.5,
                        "higher_is_better": True,
                    },
                },
            },
        )