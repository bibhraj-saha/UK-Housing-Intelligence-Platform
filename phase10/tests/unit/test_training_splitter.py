from __future__ import annotations

import pandas as pd
import pytest

from uk_housing_ml.training.splitter import (
    chronological_split,
)


def _build_monthly_dataframe(
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "period_end": (
                pd.date_range(
                    "2023-01-31",
                    periods=12,
                    freq="ME",
                )
            ),
            "feature": list(
                range(12)
            ),
            "target": list(
                range(100, 112)
            ),
        }
    )


def test_chronological_split_preserves_time_order(
) -> None:
    dataframe = (
        _build_monthly_dataframe()
    )

    result = chronological_split(
        dataframe,
        timestamp_column="period_end",
        train_fraction=0.70,
        validation_fraction=0.15,
        test_fraction=0.15,
    )

    assert (
        result.train[
            "period_end"
        ].max()
        <
        result.validation[
            "period_end"
        ].min()
    )

    assert (
        result.validation[
            "period_end"
        ].max()
        <
        result.test[
            "period_end"
        ].min()
    )


def test_split_fractions_must_sum_to_one(
) -> None:
    dataframe = (
        _build_monthly_dataframe()
    )

    with pytest.raises(
        ValueError,
        match="sum to 1.0",
    ):
        chronological_split(
            dataframe,
            timestamp_column="period_end",
            train_fraction=0.70,
            validation_fraction=0.20,
            test_fraction=0.20,
        )


def test_empty_dataset_is_rejected(
) -> None:
    dataframe = pd.DataFrame(
        columns=[
            "period_end",
            "feature",
        ]
    )

    with pytest.raises(
        ValueError,
        match="empty",
    ):
        chronological_split(
            dataframe,
            timestamp_column="period_end",
            train_fraction=0.70,
            validation_fraction=0.15,
            test_fraction=0.15,
        )