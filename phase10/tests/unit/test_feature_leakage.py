from __future__ import annotations

from uk_housing_ml.features.leakage import (
    validate_feature_columns,
)


def test_leakage_check_rejects_future_columns(
) -> None:
    result = validate_feature_columns(
        [
            "price_lag_1m",
            "future_price",
            "crime_score",
        ],
        target_column="future_price",
    )

    assert result.is_valid is False

    assert (
        "future_price"
        in result.rejected_columns
    )

    assert (
        "price_lag_1m"
        in result.approved_columns
    )


def test_leakage_check_rejects_target_column(
) -> None:
    result = validate_feature_columns(
        [
            "price_lag_1m",
            "future_price_growth",
        ],
        target_column=(
            "future_price_growth"
        ),
    )

    assert (
        "future_price_growth"
        in result.rejected_columns
    )


def test_leakage_check_accepts_historical_features(
) -> None:
    result = validate_feature_columns(
        [
            "price_lag_1m",
            "price_lag_3m",
            "price_rolling_mean_3m",
        ],
        target_column="future_price",
    )

    assert result.is_valid is True
    assert result.rejected_columns == []