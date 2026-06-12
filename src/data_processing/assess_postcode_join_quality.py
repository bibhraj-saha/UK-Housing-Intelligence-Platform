"""
Postcode Join Quality Assessment

Purpose:
1. Measure postcode join coverage
2. Identify unmatched postcodes
3. Calculate join success rate
"""

# Import pandas
import pandas as pd

# Import pathlib
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

print("\nLoading property postcodes...")

# Load only postcode column
property_df = pd.read_csv(
    PROJECT_ROOT
    / "data"
    / "processed"
    / "property_prices_clean.csv",
    usecols=["postcode"]
)

print("Loading postcode directory...")

# Load only postcode column
postcode_df = pd.read_csv(
    PROJECT_ROOT
    / "data"
    / "processed"
    / "postcodes_clean.csv",
    usecols=["postcode"]
)

# Create postcode lookup set
postcode_lookup = set(
    postcode_df["postcode"]
    .dropna()
)

print("\nCalculating matches...")

# Check whether each property postcode exists
property_df["postcode_match"] = (
    property_df["postcode"]
    .isin(postcode_lookup)
)

# Totals
total_records = len(property_df)

matched_records = (
    property_df["postcode_match"]
    .sum()
)

unmatched_records = (
    total_records
    - matched_records
)

join_success_rate = (
    matched_records
    / total_records
    * 100
)

print("\n=== JOIN QUALITY REPORT ===")

print(
    f"Total Property Records: "
    f"{total_records:,}"
)

print(
    f"Matched Records: "
    f"{matched_records:,}"
)

print(
    f"Unmatched Records: "
    f"{unmatched_records:,}"
)

print(
    f"Join Success Rate: "
    f"{join_success_rate:.2f}%"
)

# Show sample unmatched postcodes
unmatched = (
    property_df[
        ~property_df["postcode_match"]
    ]
    .head(20)
)

print("\n=== SAMPLE UNMATCHED POSTCODES ===")

print(unmatched)