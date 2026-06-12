"""
Investigate unmatched property postcodes
"""

# Import pandas
import pandas as pd

# Import pathlib
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load property data
property_df = pd.read_csv(
    PROJECT_ROOT
    / "data"
    / "processed"
    / "property_prices_clean.csv",
    usecols=["postcode"]
)

# Load postcode data
postcode_df = pd.read_csv(
    PROJECT_ROOT
    / "data"
    / "processed"
    / "postcodes_clean.csv",
    usecols=["postcode"]
)

postcode_lookup = set(
    postcode_df["postcode"].dropna()
)

property_df["matched"] = (
    property_df["postcode"]
    .isin(postcode_lookup)
)

unmatched = property_df[
    ~property_df["matched"]
]

print("\nTotal unmatched:")
print(len(unmatched))

print("\nNull postcodes:")
print(unmatched["postcode"].isna().sum())

print("\nNon-null unmatched:")
print(
    unmatched["postcode"]
    .notna()
    .sum()
)

print("\nSample non-null unmatched:")
print(
    unmatched[
        unmatched["postcode"].notna()
    ]
    .head(20)
)