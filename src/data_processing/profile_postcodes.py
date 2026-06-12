"""
Postcode Dataset Profiling

Purpose:
1. Inspect postcode directory structure
2. Identify columns
3. Understand geographic linkage fields
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

print("\nLoading postcode directory...")

# Load first few rows
df = pd.read_csv(
    INPUT_FILE,
    nrows=5
)

print("\n=== SHAPE ===")
print(df.shape)

print("\n=== COLUMN COUNT ===")
print(len(df.columns))

print("\n=== COLUMNS ===")
print(df.columns.tolist())

print("\n=== SAMPLE DATA ===")
print(df.head())