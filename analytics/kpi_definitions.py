"""
KPI Definitions
UK Housing Intelligence Platform

This file contains all business KPIs used by the analytics layer.
"""


HOUSING_KPIS = {
    "average_property_price":
        "Average property price within an area",

    "median_property_price":
        "Median property price within an area",

    "property_price_rank":
        "Ranking based on property prices"
}


CRIME_KPIS = {
    "total_crime":
        "Total crimes recorded",

    "crime_rate":
        "Crime count relative to population",

    "crime_rank":
        "Ranking based on crime levels"
}


GROWTH_KPIS = {
    "growth_score":
        "Area growth potential score",

    "growth_rank":
        "Ranking based on growth potential"
}


INVESTMENT_KPIS = {
    "investment_score":
        "Investment attractiveness score",

    "investment_rank":
        "Ranking based on investment potential"
}


PLATFORM_KPIS = {
    "housing_intelligence_index":
        "Overall intelligence score",

    "area_rank":
        "Overall area ranking",

    "percentile_rank":
        "Percentile ranking"
}