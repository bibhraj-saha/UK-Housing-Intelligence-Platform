from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class ChronologicalSplitResult:
    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame
    train_end_timestamp: str
    validation_end_timestamp: str


def chronological_split(
    dataframe: pd.DataFrame,
    *,
    timestamp_column: str,
    train_fraction: float,
    validation_fraction: float,
    test_fraction: float,
) -> ChronologicalSplitResult:
    total_fraction = (
        train_fraction
        + validation_fraction
        + test_fraction
    )

    if abs(
        total_fraction - 1.0
    ) > 1e-9:
        raise ValueError(
            "Split fractions must sum to 1.0."
        )

    if dataframe.empty:
        raise ValueError(
            "Cannot split an empty dataset."
        )

    working = dataframe.copy()

    working[
        timestamp_column
    ] = pd.to_datetime(
        working[
            timestamp_column
        ],
        errors="coerce",
    )

    working = working.dropna(
        subset=[
            timestamp_column
        ]
    ).sort_values(
        timestamp_column
    ).reset_index(
        drop=True
    )

    unique_timestamps = (
        working[
            timestamp_column
        ]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    if len(
        unique_timestamps
    ) < 3:
        raise ValueError(
            "At least three distinct timestamps "
            "are required for chronological "
            "train/validation/test splitting."
        )

    train_boundary_index = max(
        0,
        min(
            len(unique_timestamps) - 3,
            int(
                len(unique_timestamps)
                * train_fraction
            )
            - 1,
        ),
    )

    validation_boundary_index = max(
        train_boundary_index + 1,
        min(
            len(unique_timestamps) - 2,
            int(
                len(unique_timestamps)
                * (
                    train_fraction
                    + validation_fraction
                )
            )
            - 1,
        ),
    )

    train_end = pd.Timestamp(
        unique_timestamps[
            train_boundary_index
        ]
    )

    validation_end = pd.Timestamp(
        unique_timestamps[
            validation_boundary_index
        ]
    )

    train = working[
        working[
            timestamp_column
        ] <= train_end
    ].copy()

    validation = working[
        (
            working[
                timestamp_column
            ] > train_end
        )
        & (
            working[
                timestamp_column
            ] <= validation_end
        )
    ].copy()

    test = working[
        working[
            timestamp_column
        ] > validation_end
    ].copy()

    if (
        train.empty
        or validation.empty
        or test.empty
    ):
        raise ValueError(
            "Chronological split produced "
            "an empty partition."
        )

    return ChronologicalSplitResult(
        train=train,
        validation=validation,
        test=test,
        train_end_timestamp=(
            train_end.isoformat()
        ),
        validation_end_timestamp=(
            validation_end.isoformat()
        ),
    )