from __future__ import annotations

import pandas as pd

from uk_housing_ml.training.dataset_builder import (
    _construct_target,
)


def _build_training_frame(
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "lsoa_code": [
                "A",
                "A",
                "A",
                "A",
                "A",
            ],
            "period_end": (
                pd.date_range(
                    "2023-01-31",
                    periods=5,
                    freq="ME",
                )
            ),
            "average_price": [
                100.0,
                110.0,
                120.0,
                130.0,
                140.0,
            ],
        }
    )


def test_future_price_target_uses_forward_shift(
) -> None:
    dataframe = (
        _build_training_frame()
    )

    contract = {
        "entity_key": "lsoa_code",
        "target": {
            "name": "future_price",
            "horizon_months": 2,
            "construction": "future_shift",
        },
    }

    result, target_column = (
        _construct_target(
            dataframe,
            contract=contract,
            source_price_column=(
                "average_price"
            ),
        )
    )

    assert (
        target_column
        == "future_price"
    )

    assert (
        result.loc[
            0,
            "future_price",
        ]
        == 120.0
    )


def test_future_growth_target_is_forward_looking(
) -> None:
    dataframe = (
        _build_training_frame()
    )

    contract = {
        "entity_key": "lsoa_code",
        "target": {
            "name": (
                "future_price_growth"
            ),
            "horizon_months": 2,
            "construction": (
                "future_percentage_growth"
            ),
        },
    }

    result, _ = _construct_target(
        dataframe,
        contract=contract,
        source_price_column=(
            "average_price"
        ),
    )

    assert round(
        result.loc[
            0,
            "future_price_growth",
        ],
        6,
    ) == 0.2