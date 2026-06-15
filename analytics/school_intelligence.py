import pandas as pd

print("Loading school lookup...")

schools = pd.read_csv(
    "data/reference/schools/school_lookup.csv"
)

print("School Lookup Shape:")
print(schools.shape)

print("\nLoading housing intelligence...")

housing = pd.read_parquet(
    "data/analytics/housing_intelligence.parquet",
    columns=["lsoa_code"]
)

housing_lsoas = housing[["lsoa_code"]].drop_duplicates()

print("Housing LSOAs:")
print(housing_lsoas.shape)

schools = schools[
    schools["lsoa_code"].isin(
        housing_lsoas["lsoa_code"]
    )
].copy()

print("\nSchools After Housing Filter:")
print(schools.shape)

schools["school_type"] = (
    schools["school_type"]
    .fillna("")
    .astype(str)
)

school_intelligence = (
    schools
    .groupby("lsoa_code")
    .agg(
        school_count=(
            "school_name",
            "count"
        ),
        total_pupils=(
            "pupils",
            "sum"
        )
    )
    .reset_index()
)

primary = (
    schools["school_type"]
    .str.contains(
        "Primary|Nursery|Infants",
        case=False,
        na=False
    )
)

secondary = (
    schools["school_type"]
    .str.contains(
        "Secondary",
        case=False,
        na=False
    )
)

primary_counts = (
    schools[primary]
    .groupby("lsoa_code")
    .size()
    .reset_index(name="primary_school_count")
)

secondary_counts = (
    schools[secondary]
    .groupby("lsoa_code")
    .size()
    .reset_index(name="secondary_school_count")
)

school_intelligence = school_intelligence.merge(
    primary_counts,
    on="lsoa_code",
    how="left"
)

school_intelligence = school_intelligence.merge(
    secondary_counts,
    on="lsoa_code",
    how="left"
)

school_intelligence[
    "primary_school_count"
] = (
    school_intelligence[
        "primary_school_count"
    ]
    .fillna(0)
    .astype(int)
)

school_intelligence[
    "secondary_school_count"
] = (
    school_intelligence[
        "secondary_school_count"
    ]
    .fillna(0)
    .astype(int)
)

school_intelligence[
    "average_pupils_per_school"
] = (
    school_intelligence["total_pupils"]
    /
    school_intelligence["school_count"]
)

max_schools = (
    school_intelligence["school_count"]
    .max()
)

school_intelligence[
    "school_accessibility_score"
] = (
    school_intelligence["school_count"]
    /
    max_schools
    * 100
)

school_intelligence = housing_lsoas.merge(
    school_intelligence,
    on="lsoa_code",
    how="left"
)

numeric_cols = [
    "school_count",
    "primary_school_count",
    "secondary_school_count",
    "total_pupils",
    "average_pupils_per_school",
    "school_accessibility_score"
]

for col in numeric_cols:
    school_intelligence[col] = (
        school_intelligence[col]
        .fillna(0)
    )

output_file = (
    "data/analytics/"
    "school_intelligence.parquet"
)

school_intelligence.to_parquet(
    output_file,
    index=False
)

print("\nSchool Intelligence Created")

print("\nShape:")
print(school_intelligence.shape)

print("\nColumns:")
print(
    school_intelligence.columns.tolist()
)

print("\nSample:")
print(
    school_intelligence.head()
)