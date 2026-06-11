# Crime Dataset Profile

## Dataset Overview

The Crime dataset was sourced from UK Police street-level crime data for April 2026.

### Dataset Statistics

* Total Records: 478,865
* Total Columns: 12
* Coverage Period: April 2026

### Key Fields

| Field                 | Description                  |
| --------------------- | ---------------------------- |
| Crime ID              | Unique crime identifier      |
| Month                 | Reporting month              |
| Falls within          | Police force jurisdiction    |
| Longitude             | Geographic longitude         |
| Latitude              | Geographic latitude          |
| LSOA code             | Lower Super Output Area code |
| LSOA name             | Lower Super Output Area name |
| Crime type            | Crime category               |
| Last outcome category | Investigation outcome        |

---

## Exploratory Data Analysis

### Crime Category Analysis

The most frequently recorded crime category was:

* Violence and sexual offences: 165,101 incidents

This represented approximately 34.5% of all recorded crimes.

Visualisations:

* top_10_crime_categories.png
* top_5_crime_categories.png

---

### Police Force Analysis

Crime volumes were analysed across police force jurisdictions.

The Metropolitan Police Service recorded the highest number of incidents:

* 91,664 incidents

representing approximately 19.1% of all crimes in the dataset.

Visualisation:

* crime_by_police_force.png

---

### Geographic Analysis

Crime counts were aggregated by LSOA area.

Visualisation:

* top_20_crime_areas.png

This analysis highlights geographic concentrations of reported crime.

---

### Crime Outcome Analysis

The most common outcome category was:

* Under investigation: 200,723 incidents

representing approximately 51.3% of all crimes with recorded outcomes.

Visualisation:

* crime_outcomes.png

---

## Key Findings

1. Violence and sexual offences represent the largest crime category.

2. The Metropolitan Police Service accounts for the largest share of recorded crime.

3. A significant proportion of investigations remain ongoing.

4. Geographic crime concentrations can be identified at the LSOA level.

---

## Outputs Generated

* outputs/plots/top_10_crime_categories.png
* outputs/plots/top_5_crime_categories.png
* outputs/plots/top_20_crime_areas.png
* outputs/plots/crime_by_police_force.png
* outputs/plots/crime_outcomes.png

---

## Next Steps

The crime dataset will be validated and integrated with housing data to support location-based intelligence and housing market analytics.