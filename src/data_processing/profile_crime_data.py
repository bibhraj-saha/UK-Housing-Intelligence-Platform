"""
Crime Dataset Profiling

Purpose:
1. Inspect crime data structure
2. Identify columns
3. Identify datatypes
4. Understand cleaning requirements
"""

# Import pandas
import pandas as pd

# Import pathlib
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Example crime file
INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "external"
    / "crime"
    / "2026-04"
    / "2026-04-metropolitan-street.csv"
)

# Load sample
df = pd.read_csv(INPUT_FILE)

print("\n=== SHAPE ===")
print(df.shape)

print("\n=== COLUMNS ===")
print(df.columns.tolist())

print("\n=== DATA TYPES ===")
print(df.dtypes)

print("\n=== SAMPLE DATA ===")
print(df.head())