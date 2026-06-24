Modeling Standards

Naming Conventions

Dimensions:

DIM_

Examples:

DIM_LOCATION
DIM_REGION
DIM_DATE

⸻

Facts:

FCT_

Examples:

FCT_HOUSING_INTELLIGENCE
FCT_HOUSING_TRENDS

⸻

Analytics Marts:

MART_<BUSINESS_USE_CASE>

Examples:

MART_AREA_PROFILE
MART_AREA_RANKINGS

⸻

Keys

Surrogate Keys:

*_KEY

Examples:

LOCATION_KEY
REGION_KEY

⸻

Business Keys

Examples:

LSOA_CODE
LAD_CODE

⸻

Join Rules

Facts join to dimensions using surrogate keys.

Business keys are used only during transformation.