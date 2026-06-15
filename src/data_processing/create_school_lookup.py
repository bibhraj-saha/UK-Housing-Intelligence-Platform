import pandas as pd

print("Loading England schools...")

england = pd.read_csv(
    "data/external/schools/edubasealldata20260615.csv",
    encoding="cp1252",
    low_memory=False,
   usecols=[
    "EstablishmentName",
    "PhaseOfEducation (name)",
    "TypeOfEstablishment (name)",
    "NumberOfPupils",
    "LSOA (code)",
    "EstablishmentStatus (name)"
    ]
)

excluded_types = [
    "British schools overseas",
    "Offshore schools",
    "Service children's education"
]

england = england[
    (england["EstablishmentStatus (name)"] == "Open")
    &
    (~england["TypeOfEstablishment (name)"].isin(excluded_types))
].copy()

england = england.rename(
    columns={
        "EstablishmentName": "school_name",
        "PhaseOfEducation (name)": "school_type",
        "NumberOfPupils": "pupils",
        "LSOA (code)": "lsoa_code"
    }
)

england["country"] = "England"

england = england[
    [
        "school_name",
        "school_type",
        "country",
        "lsoa_code",
        "pupils"
    ]
]

print("England Shape:")
print(england.shape)

print("\nLoading Wales schools...")

wales = pd.read_csv(
    "data/external/schools/wales/maintained_schools_wg.csv",
    low_memory=False,
    usecols=[
        "school_name",
        "school_type",
        "pupils",
        "postcode"
    ]
)

postcode_lookup = pd.read_csv(
    "data/reference/postcodes/ONS_Postcode_Directory_(February_2026)_for_the_UK_(Hosted_Table).csv",
    low_memory=False,
    usecols=[
        "pcds",
        "lsoa21cd"
    ]
)

postcode_lookup["pcds"] = (
    postcode_lookup["pcds"]
    .astype(str)
    .str.upper()
    .str.strip()
)

wales["postcode"] = (
    wales["postcode"]
    .astype(str)
    .str.upper()
    .str.strip()
)

wales = wales.merge(
    postcode_lookup,
    left_on="postcode",
    right_on="pcds",
    how="left"
)

wales = wales.rename(
    columns={
        "lsoa21cd": "lsoa_code"
    }
)

wales["country"] = "Wales"

wales = wales[
    [
        "school_name",
        "school_type",
        "country",
        "lsoa_code",
        "pupils"
    ]
]

print("Wales Shape:")
print(wales.shape)

schools = pd.concat(
    [
        england,
        wales
    ],
    ignore_index=True
)

schools = schools.dropna(
    subset=["lsoa_code"]
)

schools["pupils"] = (
    schools["pupils"]
    .fillna(0)
)

schools["pupils"] = (
    schools["pupils"]
    .astype(int)
)

output_file = (
    "data/reference/schools/"
    "school_lookup.csv"
)

schools.to_csv(
    output_file,
    index=False
)

print("\nSchool Lookup Created")

print("\nShape:")
print(schools.shape)

print("\nColumns:")
print(schools.columns.tolist())

print("\nMissing LSOA:")
print(
    schools["lsoa_code"]
    .isna()
    .sum()
)

print("\nSample:")
print(
    schools.head()
)