import pandas as pd

# ==========================================
# LOAD FILES
# ==========================================

geo = pd.read_csv(
    "data/reference/geography/lsoa_geography_lookup.csv"
)

lad = pd.read_csv(
    "data/reference/geography/local_authority_lookup.csv"
)

region = pd.read_csv(
    "data/reference/geography/region_lookup.csv"
)

country = pd.read_csv(
    "data/reference/geography/country_lookup.csv"
)

# ==========================================
# CLEAN LOOKUPS
# ==========================================

lad = lad[
    ["LAD25CD", "LAD25NM"]
].rename(
    columns={
        "LAD25CD": "lad_code",
        "LAD25NM": "local_authority"
    }
)

region = region[
    ["RGN25CD", "RGN25NM"]
].rename(
    columns={
        "RGN25CD": "region_code",
        "RGN25NM": "region"
    }
)

country = country[
    ["CTRY25CD", "CTRY25NM"]
].rename(
    columns={
        "CTRY25CD": "country_code",
        "CTRY25NM": "country"
    }
)

# ==========================================
# UK-WIDE SPECIAL REGIONS
# ==========================================

special_regions = pd.DataFrame(
    {
        "region_code": [
            "S99999999",
            "W99999999",
            "N99999999",
            "L99999999",
            "M99999999"
        ],
        "region": [
            "Scotland",
            "Wales",
            "Northern Ireland",
            "Channel Islands",
            "Isle of Man"
        ]
    }
)

region = pd.concat(
    [region, special_regions],
    ignore_index=True
)

# ==========================================
# UK-WIDE SPECIAL COUNTRIES
# ==========================================

special_countries = pd.DataFrame(
    {
        "country_code": [
            "L93000001",
            "M83000003"
        ],
        "country": [
            "Channel Islands",
            "Isle of Man"
        ]
    }
)

country = pd.concat(
    [country, special_countries],
    ignore_index=True
)

# ==========================================
# MERGE
# ==========================================

geo = geo.merge(
    lad,
    on="lad_code",
    how="left"
)

geo = geo.merge(
    region,
    on="region_code",
    how="left"
)

geo = geo.merge(
    country,
    on="country_code",
    how="left"
)

# ==========================================
# SAVE
# ==========================================

geo.to_csv(
    "data/reference/geography/geography_master_lookup.csv",
    index=False
)

print("\nCreated geography_master_lookup.csv")

print("\nShape:")
print(geo.shape)

print("\nColumns:")
print(list(geo.columns))

print("\nNull counts:")
print(
    geo[
        [
            "local_authority",
            "region",
            "country"
        ]
    ].isna().sum()
)