"""
Land Registry Dataset Profiling

Purpose:
1. Inspect column structure
2. Inspect datatypes
3. Inspect sample records
4. Understand cleaning requirements
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
    / "raw"
    / "land_registry"
    / "pp-2026.csv"
)

# Load first few rows only
df = pd.read_csv(
    INPUT_FILE,
    header=None,
    nrows=5
)

print("\n=== SAMPLE DATA ===")
print(df)

print("\n=== SHAPE ===")
print(df.shape)

print("\n=== COLUMN COUNT ===")
print(len(df.columns))