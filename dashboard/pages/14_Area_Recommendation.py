import streamlit as st

from utils.api_client import (
    check_api_connection,
    get_area_prediction,
    get_available_areas,
    get_serving_health,
)

from utils.styles import (
    apply_global_styling,
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(

    page_title="Area Recommendation",

    page_icon="🏆",

    layout="wide",

)

apply_global_styling()

st.sidebar.markdown(

    "## 🤖 Machine Learning"

)

# ==========================================================
# API STATUS
# ==========================================================

api_online = check_api_connection()

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(

    "Area Recommendation"

)

st.markdown(
    """
This dashboard provides Machine Learning-based area recommendation
predictions for UK LSOAs using the Production ML Serving Layer built during
Phase 10 and served through the FastAPI REST API developed in Phase 11.
"""
)

st.caption(

    """
Machine Learning Area Recommendation
using the Phase 10 Machine Learning
Serving Layer.
"""

)

# ==========================================================
# API STATUS
# ==========================================================

if api_online:

    st.success(

        "🟢 FastAPI ML Service Connected"

    )

else:

    st.error(

        "🔴 FastAPI ML Service Offline"

    )

    st.stop()

with st.expander(
    "Area Recommendation Workflow"
):

    st.markdown(
        """
### Workflow

1. Select an LSOA.

2. Streamlit sends a request to FastAPI.

3. FastAPI retrieves the prediction from the ML Serving Layer.

4. Prediction results are displayed instantly.

No Machine Learning model is loaded inside Streamlit.
"""
    )

# ==========================================================
# SERVING STATUS
# ==========================================================

try:

    health = get_serving_health()

    col1, col2 = st.columns(2)

    col1.metric(

        "Serving Layer",

        health["status"]

    )

    col2.metric(

        "Available Areas",

        f"{health['rows']:,}"

    )

    with st.spinner(
        "Loading available areas..."
    ):

        areas = get_available_areas()

    lsoa_list = [
        area["lsoa_code"]
        for area in areas
    ]

except Exception as ex:

    st.error(

        f"Unable to connect to Serving Layer.\n\n{ex}"

    )

    st.stop()

st.divider()

# ==========================================================
# PAGE DESCRIPTION
# ==========================================================

st.subheader(

    "Machine Learning Area Recommendation"

)

st.write(

    """
This dashboard retrieves
area recommendation predictions
directly from the
Phase 10 ML Serving Layer.

No Machine Learning model
is loaded inside Streamlit.

Predictions are served through
the FastAPI REST API.
"""

)

st.subheader(
    "Select Area"
)

st.caption(
    """
Choose a UK LSOA to retrieve the latest
Machine Learning area recommendation insights.
"""
)

selected_lsoa = st.selectbox(

    "Choose an LSOA",

    options=lsoa_list,

    index=0,

)

with st.spinner(

    "Retrieving area recommendation..."

):

    prediction = get_area_prediction(
        selected_lsoa
    )

col1, col2 = st.columns(2)

with col1:

    st.success(
        "Area selected successfully."
    )

with col2:

    st.metric(
        "Selected LSOA",
        selected_lsoa,
    )

st.divider()

st.subheader(
    "Recommendation Result"
)

recommendation_score = prediction[
    "recommendation_score"
]

recommendation_rank = prediction[
    "recommendation_rank"
]

recommendation_percentile = prediction[
    "recommendation_percentile"
]

prediction_timestamp = prediction[
    "timestamp"
]

col1, col2 = st.columns(2)

col1.metric(

    "Recommendation Score",

    f"{recommendation_score:.3f}"

)

col2.metric(

    "Prediction Timestamp",

    str(prediction_timestamp)

)

st.success(
    f"""
Area recommendation successfully retrieved for

**{selected_lsoa}**

using the production Machine Learning
Serving Layer.
"""
)

st.divider()

st.subheader(
    "Prediction Summary"
)

formatted_score = (

    f"{recommendation_score:.3f}"

)

timestamp = prediction["timestamp"]

prediction_date = str(timestamp).split("T")[0]

col1, col2, col3 = st.columns(3)

col1.metric(

    "Recommendation Score",

    formatted_score,

)

col2.metric(

    "Prediction Date",

    prediction_date,

)

col3.metric(

    "ML Service",

    "Online",

)

st.divider()

col4, col5 = st.columns(2)

col4.metric(

    "Recommendation Rank",

    f"{recommendation_rank:,}"

)

col5.metric(

    "Recommendation Percentile",

    f"{recommendation_percentile:.2%}"

)

st.divider()

st.subheader(
    "Prediction Interpretation"
)

st.markdown(
    f"""
### Area Recommendation Summary

**Selected LSOA**

`{selected_lsoa}`

---

### Recommendation Score

# {formatted_score}

---

### Recommendation Rank

**{recommendation_rank:,}**

---

### Recommendation Percentile

**{recommendation_percentile:.2%}**

These recommendation metrics are generated by the
Phase 10 Machine Learning Serving Layer and exposed
through the Phase 11 FastAPI REST API.

Higher scores and percentiles indicate stronger
overall recommendations.
"""
)

st.divider()

st.subheader(
    "How to Interpret These Results"
)

st.markdown(
    """
- **Recommendation Score** is the overall Machine Learning recommendation score for the selected LSOA.

- **Recommendation Rank** shows the position of the area compared with all analysed UK LSOAs.

- **Recommendation Percentile** indicates how highly the selected area ranks relative to all other analysed areas.

Higher recommendation scores and percentiles generally indicate stronger overall investment potential.
"""
)

st.info(
    """
This dashboard performs online inference
through the REST API.

No ML model is loaded inside Streamlit.
"""
)

st.divider()

st.subheader(
    "API Response Summary"
)

summary = {

    "LSOA": selected_lsoa,

    "Prediction Date": prediction_date,

    "Recommendation Score": formatted_score,

    "Recommendation Rank": f"{recommendation_rank:,}",

    "Recommendation Percentile": f"{recommendation_percentile:.2%}",

}

st.table(summary)

st.divider()

st.caption(
    """
UK Housing Intelligence Platform

Phase 11

Machine Learning Dashboard

Powered by FastAPI • Streamlit • Snowflake • Scikit-Learn
"""
)