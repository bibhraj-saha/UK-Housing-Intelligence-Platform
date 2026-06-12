"""
Postcode Dataset Cleaning Pipeline

Purpose:
1. Load ONS postcode directory
2. Keep required columns
3. Standardize postcode values
4. Remove duplicates
5. Export cleaned dataset
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
    / "reference"
    / "postcodes"
    / "ONS_Postcode_Directory_(February_2026)_for_the_UK_(Hosted_Table).csv"
)

# Output file
OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "postcodes_clean.csv"
)

print("\nLoading postcode dataset...")

# Load dataset
df = pd.read_csv(INPUT_FILE)

print(f"Rows loaded: {len(df):,}")

# Required columns
required_columns = [
    "pcds",
    "lat",
    "long",
    "lsoa21cd",
    "msoa21cd",
    "lad25cd",
    "ctry25cd",
    "imd20ind"
]

# Keep only required columns
df = df[required_columns]

print(
    f"Columns retained: {len(df.columns)}"
)

# Rename columns
df = df.rename(
    columns={
        "pcds": "postcode",
        "lat": "latitude",
        "long": "longitude",
        "lsoa21cd": "lsoa_code",
        "msoa21cd": "msoa_code",
        "lad25cd": "local_authority_code",
        "ctry25cd": "country_code",
        "imd20ind": "deprivation_index"
    }
)

# Standardize postcode
df["postcode"] = (
    df["postcode"]
    .astype(str)
    .str.upper()
    .str.strip()
)

# Remove duplicates
before_duplicates = len(df)

df = df.drop_duplicates(
    subset=["postcode"]
)

after_duplicates = len(df)

print(
    f"Duplicates removed: "
    f"{before_duplicates - after_duplicates:,}"
)

# Remove rows with missing postcode
before_nulls = len(df)

df = df[
    df["postcode"].notna()
]

after_nulls = len(df)

print(
    f"Rows removed (null postcode): "
    f"{before_nulls - after_nulls:,}"
)

# Save dataset
df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n=== FINAL DATASET ===")
print(df.shape)

print(
    f"\nSaved to:\n{OUTPUT_FILE}"
)