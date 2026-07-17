"""Tests for ML serving dataset builder."""

import pandas as pd

from uk_housing_ml.integration.serving_builder import (
    build_area_ml_serving_dataset,
)


def test_build_area_ml_serving_dataset() -> None:
    recommendations = pd.DataFrame(
        {
            "lsoa_code": [
                "A",
                "B",
            ],
            "recommendation_rank": [
                1,
                2,
            ],
            "recommendation_score": [
                0.9,
                0.8,
            ],
        }
    )

    investment = pd.DataFrame(
        {
            "lsoa_code": [
                "A",
                "B",
            ],
            "opportunity_probability": [
                0.8,
                0.6,
            ],
        }
    )

    price = pd.DataFrame(
        {
            "lsoa_code": [
                "A",
                "B",
            ],
            "prediction": [
                200000.0,
                180000.0,
            ],
        }
    )

    growth = pd.DataFrame(
        {
            "lsoa_code": [
                "A",
                "B",
            ],
            "prediction": [
                0.1,
                0.05,
            ],
        }
    )

    result = (
        build_area_ml_serving_dataset(
            recommendations=(
                recommendations
            ),
            investment_predictions=(
                investment
            ),
            price_predictions=price,
            growth_predictions=growth,
        )
    )

    assert len(result) == 2

    assert (
        "predicted_future_price"
        in result.columns
    )

    assert (
        "predicted_future_growth"
        in result.columns
    )

    assert (
        "opportunity_probability"
        in result.columns
    )