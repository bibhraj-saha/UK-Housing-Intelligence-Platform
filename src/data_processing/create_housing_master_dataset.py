"""
Housing Master Dataset

Purpose:
1. Join property geography data
2. Join crime summary data
3. Create unified analytical dataset
"""

# Import pandas
import pandas as pd

# Import pathlib
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Input files
PROPERTY_GEO_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "property_geography.csv"
)

CRIME_SUMMARY_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "crime_lsoa_summary.csv"
)

# Output file
OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "housing_master_dataset.csv"
)

print("\nLoading property geography dataset...")

property_geo_df = pd.read_csv(
    PROPERTY_GEO_FILE
)

print(
    f"Property rows: {len(property_geo_df):,}"
)

print("\nLoading crime summary dataset...")

crime_df = pd.read_csv(
    CRIME_SUMMARY_FILE
)

print(
    f"Crime summary rows: {len(crime_df):,}"
)

print("\nJoining datasets...")

master_df = property_geo_df.merge(
    crime_df,
    on="lsoa_code",
    how="left"
)

# Replace missing crime values
crime_columns = [
    "total_crimes",
    "high_severity_crimes",
    "medium_severity_crimes",
    "low_severity_crimes"
]

master_df[crime_columns] = (
    master_df[crime_columns]
    .fillna(0)
)

print("\nCreating analytical features...")

# Crime score
master_df["crime_score"] = (
    master_df["total_crimes"]
)

# Price per crime ratio
master_df["price_to_crime_ratio"] = (
    master_df["price"]
    /
    (
        master_df["total_crimes"] + 1
    )
)

print("\nSaving dataset...")

master_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n=== FINAL DATASET ===")
print(master_df.shape)

print(
    f"\nSaved to:\n{OUTPUT_FILE}"
)