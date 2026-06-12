"""
Property Geography Dataset

Purpose:
1. Join property data with postcode geography
2. Enrich property transactions
3. Export integrated dataset
"""

# Import pandas
import pandas as pd

# Import pathlib
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Input files
PROPERTY_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "property_prices_clean.csv"
)

POSTCODE_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "postcodes_clean.csv"
)

# Output file
OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "property_geography.csv"
)

print("\nLoading property dataset...")

property_df = pd.read_csv(
    PROPERTY_FILE
)

print(
    f"Property rows: {len(property_df):,}"
)

print("\nLoading postcode dataset...")

postcode_df = pd.read_csv(
    POSTCODE_FILE
)

print(
    f"Postcode rows: {len(postcode_df):,}"
)

print("\nJoining datasets...")

property_geo_df = property_df.merge(
    postcode_df,
    on="postcode",
    how="left"
)

print(
    f"Output rows: {len(property_geo_df):,}"
)

print("\nCalculating enrichment coverage...")

matched_rows = (
    property_geo_df["lsoa_code"]
    .notna()
    .sum()
)

coverage = (
    matched_rows
    / len(property_geo_df)
    * 100
)

print(
    f"Geographic enrichment rate: "
    f"{coverage:.2f}%"
)

print("\nSaving dataset...")

property_geo_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n=== FINAL DATASET ===")
print(property_geo_df.shape)

print(
    f"\nSaved to:\n{OUTPUT_FILE}"
)