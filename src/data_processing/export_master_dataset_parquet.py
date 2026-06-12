"""
Export Housing Master Dataset to Parquet

Purpose:
1. Load master dataset
2. Export to Parquet format
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

# Output file
OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "housing_master_dataset.parquet"
)

print("\nLoading master dataset...")

df = pd.read_csv(INPUT_FILE)

print(
    f"Rows loaded: {len(df):,}"
)

print("\nExporting Parquet file...")

# Export parquet
df.to_parquet(
    OUTPUT_FILE,
    index=False
)

print("\nExport completed.")

print(
    f"\nSaved to:\n{OUTPUT_FILE}"
)