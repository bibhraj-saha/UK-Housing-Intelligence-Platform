"""
Property Price Cleaning Pipeline

Purpose:
1. Load Land Registry property datasets
2. Apply official column names
3. Combine all years
4. Remove duplicates
5. Validate data
6. Export cleaned dataset
"""

# Import pandas
import pandas as pd

# Import pathlib
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Input directory
LAND_REGISTRY_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "land_registry"
)

# Output file
OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "property_prices_clean.csv"
)

# Official Land Registry columns
COLUMN_NAMES = [
    "transaction_id",
    "price",
    "transfer_date",
    "postcode",
    "property_type",
    "old_new",
    "duration",
    "paon",
    "saon",
    "street",
    "locality",
    "town_city",
    "district",
    "county",
    "ppd_category_type",
    "record_status"
]

# Files to process
FILES = [
    "pp-2023.csv",
    "pp-2024.csv",
    "pp-2025.csv",
    "pp-2026.csv"
]

# Store yearly dataframes
all_dfs = []

# Process each file
for file_name in FILES:

    file_path = LAND_REGISTRY_DIR / file_name

    print(f"\nLoading {file_name}...")

    # Load CSV
    df = pd.read_csv(
        file_path,
        header=None,
        names=COLUMN_NAMES
    )

    print(f"Rows loaded: {len(df):,}")

    # Add source year
    df["source_file"] = file_name

    all_dfs.append(df)

# Combine all years
print("\nCombining datasets...")

combined_df = pd.concat(
    all_dfs,
    ignore_index=True
)

print(
    f"Combined rows: {len(combined_df):,}"
)

# Convert price to numeric
combined_df["price"] = pd.to_numeric(
    combined_df["price"],
    errors="coerce"
)

# Convert transfer date
combined_df["transfer_date"] = pd.to_datetime(
    combined_df["transfer_date"],
    errors="coerce"
)

# Remove rows with invalid price
before_price_filter = len(combined_df)

combined_df = combined_df[
    combined_df["price"] > 0
]

after_price_filter = len(combined_df)

print(
    f"Removed invalid prices: "
    f"{before_price_filter - after_price_filter:,}"
)

# Remove rows with invalid dates
before_date_filter = len(combined_df)

combined_df = combined_df[
    combined_df["transfer_date"].notna()
]

after_date_filter = len(combined_df)

print(
    f"Removed invalid dates: "
    f"{before_date_filter - after_date_filter:,}"
)

# Remove duplicate transaction IDs
before_duplicates = len(combined_df)

combined_df = combined_df.drop_duplicates(
    subset=["transaction_id"]
)

after_duplicates = len(combined_df)

print(
    f"Removed duplicates: "
    f"{before_duplicates - after_duplicates:,}"
)

# --------------------------------------------------
# Feature Engineering
# --------------------------------------------------

print("\nCreating business-friendly columns...")

# Property type descriptions
property_type_map = {
    "D": "Detached",
    "S": "Semi-Detached",
    "T": "Terraced",
    "F": "Flat/Maisonette",
    "O": "Other"
}

combined_df["property_type_description"] = (
    combined_df["property_type"]
    .map(property_type_map)
)

# Ownership type
ownership_map = {
    "F": "Freehold",
    "L": "Leasehold"
}

combined_df["ownership_type"] = (
    combined_df["duration"]
    .map(ownership_map)
)

# Property age
age_map = {
    "Y": "New Build",
    "N": "Existing Property"
}

combined_df["property_age_type"] = (
    combined_df["old_new"]
    .map(age_map)
)

# Transaction year
combined_df["transfer_year"] = (
    combined_df["transfer_date"]
    .dt.year
)

# Transaction month
combined_df["transfer_month"] = (
    combined_df["transfer_date"]
    .dt.month
)

# Standardize postcode
combined_df["postcode"] = (
    combined_df["postcode"]
    .astype(str)
    .str.upper()
    .str.strip()
)

# Save cleaned data
combined_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n=== FINAL DATASET ===")
print(combined_df.shape)

print(
    f"\nSaved to:\n{OUTPUT_FILE}"
)