"""
Crime LSOA Summary Dataset

Purpose:
1. Aggregate crimes by LSOA
2. Create crime metrics
3. Export summary dataset
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
    / "crime_clean.csv"
)

# Output file
OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "crime_lsoa_summary.csv"
)

print("\nLoading crime dataset...")

crime_df = pd.read_csv(
    INPUT_FILE
)

print(
    f"Rows loaded: {len(crime_df):,}"
)

# Remove records without LSOA
crime_df = crime_df[
    crime_df["lsoa_code"].notna()
]

print(
    f"Rows with LSOA: {len(crime_df):,}"
)

print("\nAggregating crimes...")

# Total crimes per LSOA
summary_df = (
    crime_df
    .groupby("lsoa_code")
    .size()
    .reset_index(name="total_crimes")
)

# High severity crimes
high_df = (
    crime_df[
        crime_df["crime_severity"] == "High"
    ]
    .groupby("lsoa_code")
    .size()
    .reset_index(name="high_severity_crimes")
)

# Medium severity crimes
medium_df = (
    crime_df[
        crime_df["crime_severity"] == "Medium"
    ]
    .groupby("lsoa_code")
    .size()
    .reset_index(name="medium_severity_crimes")
)

# Low severity crimes
low_df = (
    crime_df[
        crime_df["crime_severity"] == "Low"
    ]
    .groupby("lsoa_code")
    .size()
    .reset_index(name="low_severity_crimes")
)

# Merge summaries
summary_df = summary_df.merge(
    high_df,
    on="lsoa_code",
    how="left"
)

summary_df = summary_df.merge(
    medium_df,
    on="lsoa_code",
    how="left"
)

summary_df = summary_df.merge(
    low_df,
    on="lsoa_code",
    how="left"
)

# Replace nulls with zero
summary_df = summary_df.fillna(0)

# Save dataset
summary_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n=== FINAL DATASET ===")
print(summary_df.shape)

print(
    f"\nSaved to:\n{OUTPUT_FILE}"
)