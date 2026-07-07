from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[3]

PHASE10_SRC = (
    PROJECT_ROOT
    / "phase10"
    / "src"
)

if str(PHASE10_SRC) not in sys.path:
    sys.path.insert(
        0,
        str(PHASE10_SRC),
    )


from uk_housing_ml.io.csv_reader import (
    CsvReadResult,
    count_csv_data_rows,
    read_csv_sample_with_row_count,
    read_csv_with_encoding_fallback,
)


def test_read_csv_uses_utf8_first(
    tmp_path: Path,
) -> None:
    csv_path = (
        tmp_path
        / "utf8.csv"
    )

    csv_path.write_text(
        "name,value\n"
        "Glasgow,1\n"
        "Café,2\n",
        encoding="utf-8",
    )

    result = (
        read_csv_with_encoding_fallback(
            csv_path,
            low_memory=False,
        )
    )

    assert isinstance(
        result,
        CsvReadResult,
    )

    assert result.encoding == "utf-8"

    assert result.dataframe.shape == (
        2,
        2,
    )

    assert (
        result.dataframe.loc[
            1,
            "name",
        ]
        == "Café"
    )


def test_read_csv_falls_back_to_cp1252(
    tmp_path: Path,
) -> None:
    csv_path = (
        tmp_path
        / "cp1252.csv"
    )

    content = (
        "school_name,value\n"
        "St John’s School,1\n"
        "King’s Academy,2\n"
    )

    csv_path.write_bytes(
        content.encode(
            "cp1252"
        )
    )

    result = (
        read_csv_with_encoding_fallback(
            csv_path,
            low_memory=False,
        )
    )

    assert result.encoding == "cp1252"

    assert result.dataframe.shape == (
        2,
        2,
    )

    assert (
        result.dataframe.loc[
            0,
            "school_name",
        ]
        == "St John’s School"
    )


def test_read_csv_respects_sample_row_limit(
    tmp_path: Path,
) -> None:
    csv_path = (
        tmp_path
        / "sample.csv"
    )

    csv_path.write_text(
        "name,value\n"
        "A,1\n"
        "B,2\n"
        "C,3\n",
        encoding="utf-8",
    )

    result = (
        read_csv_with_encoding_fallback(
            csv_path,
            nrows=2,
            low_memory=False,
        )
    )

    assert len(
        result.dataframe
    ) == 2


def test_count_csv_data_rows_uses_selected_encoding(
    tmp_path: Path,
) -> None:
    csv_path = (
        tmp_path
        / "cp1252_rows.csv"
    )

    content = (
        "school_name,value\n"
        "St John’s School,1\n"
        "King’s Academy,2\n"
        "Queen’s College,3\n"
    )

    csv_path.write_bytes(
        content.encode(
            "cp1252"
        )
    )

    row_count = count_csv_data_rows(
        csv_path,
        encoding="cp1252",
    )

    assert row_count == 3


def test_read_csv_sample_with_row_count_returns_encoding(
    tmp_path: Path,
) -> None:
    csv_path = (
        tmp_path
        / "cp1252_sample.csv"
    )

    content = (
        "school_name,value\n"
        "St John’s School,1\n"
        "King’s Academy,2\n"
        "Queen’s College,3\n"
    )

    csv_path.write_bytes(
        content.encode(
            "cp1252"
        )
    )

    (
        dataframe,
        row_count,
        encoding,
    ) = read_csv_sample_with_row_count(
        csv_path,
        sample_rows=2,
    )

    assert len(dataframe) == 2
    assert row_count == 3
    assert encoding == "cp1252"


def test_non_decode_parser_error_is_not_swallowed(
    tmp_path: Path,
) -> None:
    csv_path = (
        tmp_path
        / "bad_parser.csv"
    )

    csv_path.write_text(
        "name,value\n"
        '"unterminated,1\n',
        encoding="utf-8",
    )

    with pytest.raises(
        pd.errors.ParserError
    ):
        read_csv_with_encoding_fallback(
            csv_path,
            engine="python",
        )


def test_missing_csv_raises_file_not_found(
    tmp_path: Path,
) -> None:
    csv_path = (
        tmp_path
        / "missing.csv"
    )

    with pytest.raises(
        FileNotFoundError
    ):
        read_csv_with_encoding_fallback(
            csv_path
        )


def test_directory_path_is_rejected(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        ValueError
    ):
        read_csv_with_encoding_fallback(
            tmp_path
        )


def test_empty_encoding_list_is_rejected(
    tmp_path: Path,
) -> None:
    csv_path = (
        tmp_path
        / "sample.csv"
    )

    csv_path.write_text(
        "name,value\nA,1\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError
    ):
        read_csv_with_encoding_fallback(
            csv_path,
            encodings=[],
        )


def test_direct_encoding_kwarg_is_rejected(
    tmp_path: Path,
) -> None:
    csv_path = (
        tmp_path
        / "sample.csv"
    )

    csv_path.write_text(
        "name,value\nA,1\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError
    ):
        read_csv_with_encoding_fallback(
            csv_path,
            encoding="utf-8",
        )


def test_sample_rows_must_be_positive(
    tmp_path: Path,
) -> None:
    csv_path = (
        tmp_path
        / "sample.csv"
    )

    csv_path.write_text(
        "name,value\nA,1\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError
    ):
        read_csv_sample_with_row_count(
            csv_path,
            sample_rows=0,
        )