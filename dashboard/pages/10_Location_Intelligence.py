import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Location Intelligence",
    layout="wide"
)

st.title("Location Intelligence")

@st.cache_data
def load_data():

    location = pd.read_parquet(
        "data/analytics/location_intelligence.parquet"
    )

    housing = pd.read_parquet(
        "data/analytics/housing_intelligence.parquet",
        columns=[
            "lsoa_code",
            "local_authority",
            "region"
        ]
    )

    location = location.merge(
        housing,
        on="lsoa_code",
        how="left"
    )

    return location

df = load_data()

# =====================================
# Sidebar Filters
# =====================================

st.sidebar.header("Filters")

region_options = (
    ["All"]
    +
    sorted(
        df["region"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_region = st.sidebar.selectbox(
    "Region",
    region_options
)

if selected_region != "All":

    df = df[
        df["region"]
        == selected_region
    ]

local_authority_options = (
    ["All"]
    +
    sorted(
        df["local_authority"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_la = st.sidebar.selectbox(
    "Local Authority",
    local_authority_options
)

if selected_la != "All":

    df = df[
        df["local_authority"]
        == selected_la
    ]

score_range = st.sidebar.slider(
    "Location Score Range",
    min_value=0,
    max_value=100,
    value=(0, 100)
)

df = df[
    (
        df["location_intelligence_score"]
        >= score_range[0]
    )
    &
    (
        df["location_intelligence_score"]
        <= score_range[1]
    )
]

# =====================================
# KPI Cards
# =====================================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Highest Score",
    f"{df['location_intelligence_score'].max():.1f}"
)

c2.metric(
    "Average Score",
    f"{df['location_intelligence_score'].mean():.1f}"
)

c3.metric(
    "Schools",
    f"{int(df['school_count'].sum()):,}"
)

c4.metric(
    "Healthcare Sites",
    f"{int(df['healthcare_site_count'].sum()):,}"
)

c5.metric(
    "Transport Assets",
    f"{int(df['transport_stop_count'].sum()):,}"
)

st.divider()

# =====================================
# Score Distribution
# =====================================

st.subheader(
    "Location Intelligence Distribution"
)

fig = px.histogram(
    df,
    x="location_intelligence_score",
    nbins=40
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# Top Areas
# =====================================

st.subheader(
    "Top 20 Areas"
)

top_areas = (
    df.sort_values(
        "location_rank"
    )
    .head(20)
)

st.dataframe(
    top_areas[
        [
            "lsoa_code",
            "local_authority",
            "region",
            "location_intelligence_score",
            "location_rank"
        ]
    ],
    use_container_width=True
)

# =====================================
# Schools
# =====================================

st.subheader(
    "Top Areas By School Access"
)

schools = (
    df.sort_values(
        "school_count",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    schools[
        [
            "lsoa_code",
            "local_authority",
            "school_count",
            "total_pupils"
        ]
    ],
    use_container_width=True
)

# =====================================
# Healthcare
# =====================================

st.subheader(
    "Top Areas By Healthcare Access"
)

healthcare = (
    df.sort_values(
        "healthcare_site_count",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    healthcare[
        [
            "lsoa_code",
            "local_authority",
            "healthcare_site_count"
        ]
    ],
    use_container_width=True
)

# =====================================
# Transport
# =====================================

st.subheader(
    "Top Areas By Transport Access"
)

transport = (
    df.sort_values(
        "transport_stop_count",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    transport[
        [
            "lsoa_code",
            "local_authority",
            "transport_stop_count",
            "rail_station_count",
            "metro_station_count"
        ]
    ],
    use_container_width=True
)

# =====================================
# Component Comparison
# =====================================

st.subheader(
    "Transport vs School Access"
)

fig = px.scatter(
    df,
    x="transport_stop_count",
    y="school_count",
    size="healthcare_site_count",
    color="region",
    hover_data=[
        "local_authority",
        "lsoa_code"
    ]
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# Regional Comparison
# =====================================

st.subheader(
    "Average Location Score By Region"
)

regional = (
    df.groupby("region")
    .agg(
        avg_score=(
            "location_intelligence_score",
            "mean"
        )
    )
    .reset_index()
)

fig = px.bar(
    regional,
    x="region",
    y="avg_score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)