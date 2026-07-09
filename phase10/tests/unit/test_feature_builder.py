from __future__ import annotations

import pandas as pd

from uk_housing_ml.features.builder import (
    _apply_feature,
)
from uk_housing_ml.features.registry import (
    FeatureDefinition,
)


def _build_feature_frame(
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "lsoa_code": [
                "A",
                "A",
                "A",
                "A",
            ],
            "period_end": (
                pd.date_range(
                    "2023-01-31",
                    periods=4,
                    freq="ME",
                )
            ),
            "average_price": [
                100.0,
                110.0,
                121.0,
                133.1,
            ],
        }
    )


def test_lag_feature_uses_prior_period_only(
) -> None:
    dataframe = (
        _build_feature_frame()
    )

    definition = FeatureDefinition(
        name="price_lag_1m",
        source_role="price",
        operation="lag",
        periods=1,
    )

    result = _apply_feature(
        dataframe,
        definition=definition,
        entity_key="lsoa_code",
        source_column="average_price",
    )

    assert pd.isna(
        result.iloc[0]
    )

    assert result.iloc[1] == 100.0
    assert result.iloc[2] == 110.0


def test_rolling_mean_is_shifted_before_rolling(
) -> None:
    dataframe = (
        _build_feature_frame()
    )

    definition = FeatureDefinition(
        name="price_rolling_mean_3m",
        source_role="price",
        operation="rolling_mean",
        window=3,
        shift=1,
    )

    result = _apply_feature(
        dataframe,
        definition=definition,
        entity_key="lsoa_code",
        source_column="average_price",
    )

    assert pd.isna(
        result.iloc[0]
    )

    assert result.iloc[1] == 100.0

    assert result.iloc[2] == 105.0