import pandas as pd

INPUT_FILE = (
    "data/external/ons/ashetable82025provisional/"
    "PROV - Home Geography Table 8.1a   Weekly pay - Gross 2025.xlsx"
)

OUTPUT_FILE = (
    "data/reference/income/income_lookup.csv"
)

# =====================================================
# LOAD ASHE DATA
# =====================================================

print("Loading ASHE income dataset...")

df = pd.read_excel(
    INPUT_FILE,
    sheet_name="All",
    header=4
)

# =====================================================
# KEEP REQUIRED COLUMNS
# =====================================================

df = df[
    [
        "Description",
        "Code",
        "Median",
        "Mean"
    ]
]

# =====================================================
# RENAME COLUMNS
# =====================================================

df.columns = [
    "area_name",
    "lad_code",
    "median_weekly_income",
    "mean_weekly_income"
]

# =====================================================
# CLEAN DATA
# =====================================================

df = df.dropna(
    subset=[
        "lad_code",
        "median_weekly_income"
    ]
)

# Remove rows with unreliable values
df = df[
    ~df["median_weekly_income"]
    .astype(str)
    .isin(
        [
            "x",
            "..",
            ":",
            "-"
        ]
    )
]

# Convert to numeric
df["median_weekly_income"] = pd.to_numeric(
    df["median_weekly_income"],
    errors="coerce"
)

df["mean_weekly_income"] = pd.to_numeric(
    df["mean_weekly_income"],
    errors="coerce"
)

df = df.dropna(
    subset=[
        "median_weekly_income"
    ]
)

# =====================================================
# KEEP ENGLAND + WALES LOCAL AUTHORITIES ONLY
# =====================================================

df = df[
    df["lad_code"]
    .astype(str)
    .str.startswith(
        (
            "E",
            "W"
        )
    )
]

# =====================================================
# REMOVE REGION / COUNTRY TOTALS
# =====================================================

df = df[
    df["lad_code"]
    .str.len()
    == 9
]

# =====================================================
# CREATE ANNUAL INCOME
# =====================================================

df["estimated_annual_income"] = (
    df["median_weekly_income"]
    * 52
)

# =====================================================
# SORT
# =====================================================

df = df.sort_values(
    "lad_code"
).reset_index(
    drop=True
)

# =====================================================
# SAVE
# =====================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

# =====================================================
# VALIDATION
# =====================================================

print("\nIncome Lookup Created")

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nSample:")
print(df.head())