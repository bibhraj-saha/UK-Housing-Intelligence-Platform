import pandas as pd

print("Loading healthcare lookup...")

healthcare = pd.read_csv(
    "data/reference/healthcare/healthcare_lookup.csv"
)

print("Healthcare Shape:")
print(healthcare.shape)

print("\nLoading housing intelligence...")

housing = pd.read_parquet(
    "data/analytics/housing_intelligence.parquet",
    columns=["lsoa_code"]
)

housing_lsoas = housing[
    ["lsoa_code"]
].drop_duplicates()

print("Housing LSOAs:")
print(housing_lsoas.shape)

healthcare = healthcare[
    healthcare["lsoa_code"].isin(
        housing_lsoas["lsoa_code"]
    )
].copy()

print("\nHealthcare After Housing Filter:")
print(healthcare.shape)

healthcare_intelligence = (
    healthcare
    .groupby("lsoa_code")
    .agg(
        healthcare_site_count=(
            "site_code",
            "count"
        )
    )
    .reset_index()
)

max_sites = (
    healthcare_intelligence[
        "healthcare_site_count"
    ]
    .max()
)

healthcare_intelligence[
    "healthcare_accessibility_score"
] = (
    healthcare_intelligence[
        "healthcare_site_count"
    ]
    /
    max_sites
    * 100
)

healthcare_intelligence = (
    housing_lsoas
    .merge(
        healthcare_intelligence,
        on="lsoa_code",
        how="left"
    )
)

healthcare_intelligence[
    "healthcare_site_count"
] = (
    healthcare_intelligence[
        "healthcare_site_count"
    ]
    .fillna(0)
)

healthcare_intelligence[
    "healthcare_accessibility_score"
] = (
    healthcare_intelligence[
        "healthcare_accessibility_score"
    ]
    .fillna(0)
)

output_file = (
    "data/analytics/"
    "healthcare_intelligence.parquet"
)

healthcare_intelligence.to_parquet(
    output_file,
    index=False
)

print("\nHealthcare Intelligence Created")

print("\nShape:")
print(healthcare_intelligence.shape)

print("\nColumns:")
print(
    healthcare_intelligence.columns.tolist()
)

print("\nSample:")
print(
    healthcare_intelligence.head()
)