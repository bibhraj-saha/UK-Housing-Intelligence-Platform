"""
Verify Integration Keys

Purpose:
Ensure datasets can be joined safely.
"""

# Import pandas
import pandas as pd

# Import pathlib
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Property dataset
property_df = pd.read_csv(
    PROJECT_ROOT
    / "data"
    / "processed"
    / "property_prices_clean.csv",
    usecols=["postcode"]
)

# Postcode dataset
postcode_df = pd.read_csv(
    PROJECT_ROOT
    / "data"
    / "processed"
    / "postcodes_clean.csv",
    usecols=["postcode"]
)

print("\nProperty postcodes:")
print(property_df["postcode"].nunique())

print("\nPostcode directory postcodes:")
print(postcode_df["postcode"].nunique())

# Sample overlap check
property_postcodes = set(
    property_df["postcode"]
    .dropna()
    .head(10000)
)

postcode_directory = set(
    postcode_df["postcode"]
    .dropna()
)

matches = len(
    property_postcodes.intersection(
        postcode_directory
    )
)

print(
    f"\nMatches found in sample: "
    f"{matches:,}"
)