"""Load Step 3 training datasets."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


_SPLIT_ALIASES = {
    "train": [
        "train.parquet",
        "training.parquet",
        "train_dataset.parquet",
    ],
    "validation": [
        "validation.parquet",
        "val.parquet",
        "validation_dataset.parquet",
    ],
    "test": [
        "test.parquet",
        "test_dataset.parquet",
    ],
}


def _resolve_split_path(
    dataset_directory: Path,
    split_name: str,
) -> Path:
    aliases = _SPLIT_ALIASES[
        split_name
    ]

    for file_name in aliases:
        candidate = (
            dataset_directory
            / file_name
        )

        if candidate.is_file():
            return candidate

    wildcard_matches = sorted(
        dataset_directory.glob(
            f"*{split_name}*.parquet"
        )
    )

    if len(wildcard_matches) == 1:
        return wildcard_matches[0]

    available = sorted(
        path.name
        for path in dataset_directory.glob(
            "*.parquet"
        )
    )

    raise FileNotFoundError(
        "Could not resolve "
        f"'{split_name}' split in "
        f"{dataset_directory}. "
        f"Available parquet files: "
        f"{available}"
    )


def load_training_splits(
    dataset_directory: Path,
) -> dict[str, pd.DataFrame]:
    """Load chronological training splits."""

    dataset_directory = (
        Path(dataset_directory)
    )

    if not dataset_directory.is_dir():
        raise FileNotFoundError(
            "Training dataset directory "
            f"does not exist: "
            f"{dataset_directory}"
        )

    splits: dict[str, pd.DataFrame] = {}

    for split_name in (
        "train",
        "validation",
        "test",
    ):
        split_path = _resolve_split_path(
            dataset_directory=(
                dataset_directory
            ),
            split_name=split_name,
        )

        frame = pd.read_parquet(
            split_path
        )

        if frame.empty:
            raise ValueError(
                f"{split_name} split is empty."
            )

        splits[split_name] = frame

    return splits