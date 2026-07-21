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

    page_title="Growth Prediction",

    page_icon="📈",

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

    "Growth Prediction"

)

st.markdown(
    """
This dashboard provides Machine Learning-based future house price growth
predictions for UK LSOAs using the Production ML Serving Layer built during
Phase 10 and served through the FastAPI REST API developed in Phase 11.
"""
)

st.caption(

    """
Future UK House Price Growth
Prediction using the Phase 10
Machine Learning Serving Layer.
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
    "Growth Prediction Workflow"
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

    "Machine Learning Growth Prediction"

)

st.write(

    """
This dashboard retrieves
future house price growth predictions
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
Machine Learning growth prediction.
"""
)

selected_lsoa = st.selectbox(

    "Choose an LSOA",

    options=lsoa_list,

    index=0,

)

with st.spinner(

    "Retrieving growth prediction..."

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
    "Prediction Result"
)

prediction_growth = prediction[
    "predicted_future_growth"
]

prediction_timestamp = prediction[
    "timestamp"
]

col1, col2 = st.columns(2)

col1.metric(

    "Predicted Future Growth",

    f"{prediction_growth:.2%}"

)

col2.metric(

    "Prediction Timestamp",

    str(prediction_timestamp)

)

st.success(
    f"""
Growth prediction successfully retrieved for

**{selected_lsoa}**

using the production Machine Learning
Serving Layer.
"""
)

st.divider()

st.subheader(
    "Prediction Summary"
)

growth = prediction["predicted_future_growth"]

timestamp = prediction["timestamp"]

formatted_growth = f"{growth:.2%}"

prediction_date = str(timestamp).split("T")[0]

investment_probability = prediction[
    "opportunity_probability"
]

recommendation_score = prediction[
    "recommendation_score"
]

recommendation_rank = prediction[
    "recommendation_rank"
]

recommendation_percentile = prediction[
    "recommendation_percentile"
]

col1, col2, col3 = st.columns(3)

col1.metric(

    "Predicted Growth",

    formatted_growth,

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

col4, col5, col6 = st.columns(3)

col4.metric(

    "Prediction Source",

    "ML Serving Layer",

)

col5.metric(

    "Investment Probability",

    f"{investment_probability:.2%}",

)

col6.metric(

    "Recommendation Score",

    f"{recommendation_score:.3f}",

)

st.divider()

col7, col8 = st.columns(2)

col7.metric(

    "Recommendation Rank",

    f"{recommendation_rank:,}",

)

col8.metric(

    "Recommendation Percentile",

    f"{recommendation_percentile:.2%}",

)

st.divider()

st.subheader(
    "Prediction Interpretation"
)

st.markdown(
    f"""
### ML Prediction Summary

**Selected LSOA**

`{selected_lsoa}`

---

### Predicted Future Growth

# {formatted_growth}

---

### Investment Opportunity Probability

**{investment_probability:.2%}**

---

### Recommendation Score

**{recommendation_score:.3f}**

---

### Recommendation Rank

**{recommendation_rank:,}**

These values are served directly from the
Phase 10 ML Serving Layer through the
Phase 11 FastAPI REST API.
"""
)

st.divider()

st.subheader(
    "How to Interpret These Results"
)

st.markdown(
    """
- **Predicted Future Growth** represents the expected percentage growth in house prices.

- **Investment Probability** indicates the likelihood that the area represents a strong investment opportunity.

- **Recommendation Score** is the overall ML ranking score.

These metrics should be interpreted together rather than individually.
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

    "Predicted Growth": formatted_growth,

    "Investment Probability": f"{investment_probability:.2%}",

    "Recommendation Score": f"{recommendation_score:.3f}",

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