"""
Housing Master Dataset Validation

Purpose:
1. Validate row counts
2. Validate null values
3. Validate duplicates
4. Validate enrichment coverage
"""

# Import pandas
import pandas as pd

# Import pathlib
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Input file
INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "housing_master_dataset.csv"
)

print("\nLoading housing master dataset...")

df = pd.read_csv(INPUT_FILE)

print("\n=== DATASET SHAPE ===")
print(df.shape)

# --------------------------------------------------
# Duplicate Check
# --------------------------------------------------

duplicate_count = (
    df["transaction_id"]
    .duplicated()
    .sum()
)

print("\n=== DUPLICATES ===")
print(
    f"Duplicate transaction IDs: "
    f"{duplicate_count:,}"
)

# --------------------------------------------------
# Null Checks
# --------------------------------------------------

critical_columns = [
    "price",
    "postcode",
    "lsoa_code",
    "latitude",
    "longitude"
]

print("\n=== NULL VALUES ===")

for column in critical_columns:

    null_count = (
        df[column]
        .isna()
        .sum()
    )

    null_percent = (
        null_count
        / len(df)
        * 100
    )

    print(
        f"{column}: "
        f"{null_count:,} "
        f"({null_percent:.2f}%)"
    )

# --------------------------------------------------
# Geographic Coverage
# --------------------------------------------------

geo_matches = (
    df["lsoa_code"]
    .notna()
    .sum()
)

geo_coverage = (
    geo_matches
    / len(df)
    * 100
)

print("\n=== GEOGRAPHIC COVERAGE ===")

print(
    f"Coverage: "
    f"{geo_coverage:.2f}%"
)

# --------------------------------------------------
# Crime Validation
# --------------------------------------------------

crime_records = (
    df["total_crimes"]
    .gt(0)
    .sum()
)

crime_percent = (
    crime_records
    / len(df)
    * 100
)

print("\n=== CRIME COVERAGE ===")

print(
    f"Rows with crime metrics: "
    f"{crime_records:,}"
)

print(
    f"Coverage: "
    f"{crime_percent:.2f}%"
)

print("\nValidation completed.")