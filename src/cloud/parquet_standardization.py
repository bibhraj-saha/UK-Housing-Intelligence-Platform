from pathlib import Path
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"


FILES_TO_CONVERT = [
    "property_prices_clean.csv",
    "crime_lsoa_summary.csv",
    "postcodes_clean.csv",
    "property_geography.csv"
]


def convert_csv_to_parquet(csv_file: Path):

    parquet_file = csv_file.with_suffix(".parquet")

    print(f"\nProcessing: {csv_file.name}")

    df = pd.read_csv(csv_file)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    table = pa.Table.from_pandas(df)

    pq.write_table(
        table,
        parquet_file,
        compression="snappy"
    )

    csv_size = csv_file.stat().st_size / (1024 * 1024)
    parquet_size = parquet_file.stat().st_size / (1024 * 1024)

    reduction = (
        (csv_size - parquet_size)
        / csv_size
    ) * 100

    print(f"CSV Size      : {csv_size:.2f} MB")
    print(f"Parquet Size  : {parquet_size:.2f} MB")
    print(f"Reduction     : {reduction:.2f}%")

    return parquet_file


def main():

    print("=" * 60)
    print("PHASE 7 - PARQUET STANDARDIZATION")
    print("=" * 60)

    created_files = []

    for file_name in FILES_TO_CONVERT:

        csv_path = PROCESSED_DIR / file_name

        if not csv_path.exists():
            print(f"\nMissing: {file_name}")
            continue

        parquet_file = convert_csv_to_parquet(csv_path)

        created_files.append(parquet_file)

    print("\n")
    print("=" * 60)
    print("CREATED FILES")
    print("=" * 60)

    for file in created_files:
        print(file.name)


if __name__ == "__main__":
    main()