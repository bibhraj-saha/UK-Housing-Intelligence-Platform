import pandas as pd

INPUT_FILE = (
    "data/external/ons/ashetable82025provisional/"
    "PROV - Home Geography Table 8.1a   Weekly pay - Gross 2025.xlsx"
)

OUTPUT_FILE = (
    "data/reference/income/regional_income_lookup.csv"
)

# =====================================================
# LOAD
# =====================================================

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

df.columns = [
    "region",
    "region_code",
    "median_weekly_income",
    "mean_weekly_income"
]

# =====================================================
# KEEP ENGLAND REGIONS + WALES
# =====================================================

region_codes = [
    "E12000001",
    "E12000002",
    "E12000003",
    "E12000004",
    "E12000005",
    "E12000006",
    "E12000007",
    "E12000008",
    "E12000009",
    "W92000004"
]

df = df[
    df["region_code"]
    .isin(region_codes)
]

# =====================================================
# NUMERIC
# =====================================================

df["median_weekly_income"] = pd.to_numeric(
    df["median_weekly_income"],
    errors="coerce"
)

df["mean_weekly_income"] = pd.to_numeric(
    df["mean_weekly_income"],
    errors="coerce"
)

df["estimated_annual_income"] = (
    df["median_weekly_income"] * 52
)

# =====================================================
# SAVE
# =====================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(df)