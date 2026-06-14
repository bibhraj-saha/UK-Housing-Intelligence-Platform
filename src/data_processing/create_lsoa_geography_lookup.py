import pandas as pd


INPUT_FILE = (
    "data/reference/postcodes/"
    "ONS_Postcode_Directory_(February_2026)_for_the_UK_(Hosted_Table).csv"
)

OUTPUT_FILE = (
    "data/reference/geography/"
    "lsoa_geography_lookup.csv"
)


print("Loading ONS Postcode Directory...")

df = pd.read_csv(
    INPUT_FILE,
    low_memory=False
)

print("Rows loaded:", len(df))

# ==========================================
# SELECT REQUIRED COLUMNS
# ==========================================

geo = df[
    [
        "lsoa21cd",
        "lad25cd",
        "rgn25cd",
        "ctry25cd",
        "lat",
        "long"
    ]
].copy()

# ==========================================
# REMOVE NULL LSOA RECORDS
# ==========================================

geo = geo.dropna(
    subset=["lsoa21cd"]
)

# ==========================================
# ONE RECORD PER LSOA
# ==========================================

geo = (
    geo.groupby(
        "lsoa21cd",
        as_index=False
    )
    .agg(
        {
            "lad25cd": "first",
            "rgn25cd": "first",
            "ctry25cd": "first",
            "lat": "mean",
            "long": "mean"
        }
    )
)

# ==========================================
# RENAME COLUMNS
# ==========================================

geo = geo.rename(
    columns={
        "lsoa21cd": "lsoa_code",
        "lad25cd": "lad_code",
        "rgn25cd": "region_code",
        "ctry25cd": "country_code",
        "lat": "latitude",
        "long": "longitude"
    }
)

# ==========================================
# SAVE
# ==========================================

geo.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nLookup created")

print(geo.shape)

print("\nColumns:")

print(list(geo.columns))