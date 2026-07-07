from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import pandas as pd


DEFAULT_CSV_ENCODINGS: tuple[str, ...] = (
    "utf-8",
    "cp1252",
)


@dataclass(frozen=True)
class CsvReadResult:
    dataframe: pd.DataFrame
    encoding: str


def _normalise_encodings(
    encodings: Iterable[str],
) -> tuple[str, ...]:
    normalised: list[str] = []

    for encoding in encodings:
        value = str(encoding).strip()

        if not value:
            continue

        if value not in normalised:
            normalised.append(value)

    if not normalised:
        raise ValueError(
            "At least one CSV encoding must be configured."
        )

    return tuple(normalised)


def read_csv_with_encoding_fallback(
    csv_path: Path,
    *,
    encodings: Iterable[str] = DEFAULT_CSV_ENCODINGS,
    **read_csv_kwargs: Any,
) -> CsvReadResult:
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"CSV path is not a file: {path}"
        )

    candidate_encodings = _normalise_encodings(
        encodings
    )

    if "encoding" in read_csv_kwargs:
        raise ValueError(
            "Do not pass 'encoding' through read_csv_kwargs. "
            "Use the encodings argument so fallback behavior "
            "remains explicit."
        )

    last_decode_error: UnicodeDecodeError | None = None

    for encoding in candidate_encodings:
        try:
            dataframe = pd.read_csv(
                path,
                encoding=encoding,
                **read_csv_kwargs,
            )

            return CsvReadResult(
                dataframe=dataframe,
                encoding=encoding,
            )

        except UnicodeDecodeError as exc:
            last_decode_error = exc

    if last_decode_error is not None:
        attempted = ", ".join(
            candidate_encodings
        )

        raise UnicodeDecodeError(
            last_decode_error.encoding,
            last_decode_error.object,
            last_decode_error.start,
            last_decode_error.end,
            (
                f"{last_decode_error.reason}; "
                f"CSV decoding failed for {path} "
                f"after trying encodings: {attempted}"
            ),
        ) from last_decode_error

    raise RuntimeError(
        "CSV encoding fallback reached an unexpected "
        f"state for: {path}"
    )


def count_csv_data_rows(
    csv_path: Path,
    *,
    encoding: str,
) -> int:
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"CSV path is not a file: {path}"
        )

    with path.open(
        "r",
        encoding=encoding,
        newline="",
    ) as file:
        line_count = sum(
            1
            for _ in file
        )

    return max(
        line_count - 1,
        0,
    )


def read_csv_sample_with_row_count(
    csv_path: Path,
    *,
    sample_rows: int,
    encodings: Iterable[str] = DEFAULT_CSV_ENCODINGS,
    low_memory: bool = False,
    **read_csv_kwargs: Any,
) -> tuple[
    pd.DataFrame,
    int,
    str,
]:
    if sample_rows <= 0:
        raise ValueError(
            "sample_rows must be greater than zero."
        )

    result = read_csv_with_encoding_fallback(
        csv_path,
        encodings=encodings,
        nrows=sample_rows,
        low_memory=low_memory,
        **read_csv_kwargs,
    )

    row_count = count_csv_data_rows(
        csv_path,
        encoding=result.encoding,
    )

    return (
        result.dataframe,
        row_count,
        result.encoding,
    )