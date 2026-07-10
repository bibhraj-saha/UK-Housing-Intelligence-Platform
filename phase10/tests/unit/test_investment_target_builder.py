"""Tests for investment target construction."""

import pandas as pd

from uk_housing_ml.investment.target_builder import (
    build_investment_target,
)


def test_investment_target_uses_future_growth() -> None:
    frame = pd.DataFrame(
        {
            "future_price_growth": [
                0.10,
                -0.05,
                0.00,
            ]
        }
    )

    result = build_investment_target(
        frame
    )

    assert (
        result[
            "investment_opportunity"
        ].tolist()
        == [
            1,
            0,
            0,
        ]
    )


def test_missing_future_growth_stays_missing() -> None:
    frame = pd.DataFrame(
        {
            "future_price_growth": [
                0.10,
                None,
            ]
        }
    )

    result = build_investment_target(
        frame
    )

    assert (
        result.loc[
            0,
            "investment_opportunity",
        ]
        == 1
    )

    assert pd.isna(
        result.loc[
            1,
            "investment_opportunity",
        ]
    )