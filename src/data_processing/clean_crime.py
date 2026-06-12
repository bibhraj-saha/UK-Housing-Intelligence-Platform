"""
Crime Dataset Cleaning Pipeline

Purpose:
1. Load all police force files
2. Combine datasets
3. Standardize columns
4. Create business features
5. Export cleaned crime dataset
"""

# Import pandas
import pandas as pd

# Import pathlib
from pathlib import Path

# Import glob for file discovery
from glob import glob

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Crime directory
CRIME_DIR = (
    PROJECT_ROOT
    / "data"
    / "external"
    / "crime"
    / "2026-04"
)

# Output file
OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "crime_clean.csv"
)

print("\nDiscovering crime files...")

# Find all crime CSV files
crime_files = glob(
    str(CRIME_DIR / "*-street.csv")
)

print(f"Files found: {len(crime_files)}")

# Store dataframes
all_dfs = []

# Process each file
for file_path in crime_files:

    file_name = Path(file_path).name

    print(f"Loading {file_name}...")

    # Read file
    df = pd.read_csv(file_path)

    # Store source file
    df["source_file"] = file_name

    # Add dataframe
    all_dfs.append(df)

# Combine datasets
print("\nCombining datasets...")

crime_df = pd.concat(
    all_dfs,
    ignore_index=True
)

print(f"Combined rows: {len(crime_df):,}")

# Standardize column names
crime_df.columns = (
    crime_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("Column names standardized.")

# Convert month to datetime
crime_df["month"] = pd.to_datetime(
    crime_df["month"],
    errors="coerce"
)

# Create year feature
crime_df["crime_year"] = (
    crime_df["month"]
    .dt.year
)

# Create month feature
crime_df["crime_month"] = (
    crime_df["month"]
    .dt.month
)

# Standardize crime type
crime_df["crime_type"] = (
    crime_df["crime_type"]
    .astype(str)
    .str.strip()
)

# Standardize police force name
crime_df["reported_by"] = (
    crime_df["reported_by"]
    .astype(str)
    .str.strip()
)

# Create police force feature
crime_df["police_force"] = (
    crime_df["reported_by"]
)

print("\nCreating crime severity categories...")

# Crime severity mapping
severity_map = {

    "Violence and sexual offences": "High",

    "Robbery": "High",

    "Possession of weapons": "High",

    "Burglary": "High",

    "Vehicle crime": "Medium",

    "Criminal damage and arson": "Medium",

    "Public order": "Medium",

    "Drugs": "Medium",

    "Shoplifting": "Medium",

    "Other theft": "Medium",

    "Bicycle theft": "Low",

    "Anti-social behaviour": "Low",

    "Other crime": "Low"
}

crime_df["crime_severity"] = (
    crime_df["crime_type"]
    .map(severity_map)
    .fillna("Unknown")
)

# Crime category grouping
crime_group_map = {

    "Violence and sexual offences": "Violent Crime",

    "Robbery": "Violent Crime",

    "Possession of weapons": "Violent Crime",

    "Burglary": "Property Crime",

    "Vehicle crime": "Property Crime",

    "Criminal damage and arson": "Property Crime",

    "Shoplifting": "Property Crime",

    "Other theft": "Property Crime",

    "Bicycle theft": "Property Crime",

    "Drugs": "Public Safety",

    "Public order": "Public Safety",

    "Anti-social behaviour": "Community",

    "Other crime": "Other"
}

crime_df["crime_category_group"] = (
    crime_df["crime_type"]
    .map(crime_group_map)
    .fillna("Other")
)

# Save processed dataset
crime_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n=== FINAL DATASET ===")
print(crime_df.shape)

print(
    f"\nCrime dataset saved to:\n{OUTPUT_FILE}"
)