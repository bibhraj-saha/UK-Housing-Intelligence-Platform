import pandas as pd
from pathlib import Path

print("Loading postcode lookup...")

postcode_lookup = pd.read_csv(
    "data/reference/postcodes/ONS_Postcode_Directory_(February_2026)_for_the_UK_(Hosted_Table).csv",
    usecols=["pcds", "lsoa21cd"],
    low_memory=False
)

postcode_lookup["pcds"] = (
    postcode_lookup["pcds"]
    .astype(str)
    .str.upper()
    .str.strip()
)

print("Loading England healthcare...")

eng = pd.read_csv(
    "data/external/healthcare/ets.csv",
    header=None,
    low_memory=False
)

eng = eng.rename(
    columns={
        0: "site_code",
        1: "site_name",
        9: "postcode"
    }
)

eng["country"] = "England"

eng = eng[
    [
        "site_code",
        "site_name",
        "country",
        "postcode"
    ]
]

print("Loading Wales healthcare...")

wal = pd.read_csv(
    "data/external/healthcare/wlhbsite.csv",
    header=None,
    low_memory=False
)

wal = wal.rename(
    columns={
        0: "site_code",
        1: "site_name",
        9: "postcode"
    }
)

wal["country"] = "Wales"

wal = wal[
    [
        "site_code",
        "site_name",
        "country",
        "postcode"
    ]
]

healthcare = pd.concat(
    [
        eng,
        wal
    ],
    ignore_index=True
)

healthcare["postcode"] = (
    healthcare["postcode"]
    .astype(str)
    .str.upper()
    .str.strip()
)

healthcare = healthcare.merge(
    postcode_lookup,
    left_on="postcode",
    right_on="pcds",
    how="left"
)

healthcare = healthcare.rename(
    columns={
        "lsoa21cd": "lsoa_code"
    }
)

healthcare = healthcare.dropna(
    subset=["lsoa_code"]
)

healthcare = healthcare[
    [
        "site_code",
        "site_name",
        "country",
        "postcode",
        "lsoa_code"
    ]
]

Path(
    "data/reference/healthcare"
).mkdir(
    parents=True,
    exist_ok=True
)

output_file = (
    "data/reference/healthcare/"
    "healthcare_lookup.csv"
)

healthcare.to_csv(
    output_file,
    index=False
)

print("\nHealthcare Lookup Created")

print("\nShape:")
print(healthcare.shape)

print("\nCountries:")
print(
    healthcare["country"]
    .value_counts()
)

print("\nMissing LSOA:")
print(
    healthcare["lsoa_code"]
    .isna()
    .sum()
)