"""Investment opportunity target construction."""

from __future__ import annotations

import pandas as pd


def build_investment_target(
    frame: pd.DataFrame,
    *,
    growth_column: str = "future_price_growth",
    target_column: str = "investment_opportunity",
    minimum_growth: float = 0.0,
) -> pd.DataFrame:
    """Create a binary future-growth investment target."""

    if growth_column not in frame.columns:
        raise ValueError(
            "Missing future growth column: "
            f"{growth_column}"
        )

    output = frame.copy()

    growth = pd.to_numeric(
        output[growth_column],
        errors="coerce",
    )

    output[target_column] = pd.Series(
        pd.NA,
        index=output.index,
        dtype="Int64",
    )

    valid = growth.notna()

    output.loc[
        valid,
        target_column,
    ] = (
        growth.loc[valid]
        > float(minimum_growth)
    ).astype(int)

    return output