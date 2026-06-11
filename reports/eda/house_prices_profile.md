# House Prices Dataset Profile

## Dataset Overview

The House Prices dataset was sourced from the UK Land Registry Price Paid Data and contains residential property transaction records from 2023 to 2026.

### Dataset Statistics

* Total Records: 2,816,596
* Total Columns: 16
* Data Source: UK Land Registry Price Paid Data
* Coverage Period: 2023–2026

### Key Fields

| Field            | Description                                    |
| ---------------- | ---------------------------------------------- |
| transaction_id   | Unique transaction identifier                  |
| price            | Property sale price (£)                        |
| date_of_transfer | Transaction date                               |
| postcode         | Property postcode                              |
| property_type    | Detached, Semi-Detached, Terraced, Flat, Other |
| town_city        | Town or city                                   |
| district         | Administrative district                        |
| county           | County                                         |

---

## Exploratory Data Analysis

### Price Distribution

Property prices exhibit a highly right-skewed distribution.

Most transactions occur within typical residential price ranges, while a small number of very high-value transactions create a long tail extending into hundreds of millions of pounds.

Two visualisations were created:

* price_distribution_raw.png
* price_distribution_log.png

The log-transformed distribution provides a more interpretable view of the underlying market.

---

### Geographic Analysis

Average property prices were calculated by county.

Visualisation:

* avg_price_by_county.png

This analysis highlights regional variations in housing affordability and property market value across the United Kingdom.

---

### Property Type Analysis

Property types were analysed using the property_type field.

Visualisation:

* property_type_distribution.png

This provides insight into the composition of the UK housing market and the relative prevalence of detached, semi-detached, terraced and flat properties.

---

## Key Findings

1. The housing market exhibits significant price skewness due to a relatively small number of very high-value transactions.

2. Geographic location remains a major driver of property value.

3. Property type distribution provides useful context for future housing affordability and market segmentation analysis.

---

## Outputs Generated

* outputs/plots/price_distribution_raw.png
* outputs/plots/price_distribution_log.png
* outputs/plots/avg_price_by_county.png
* outputs/plots/property_type_distribution.png

---

## Next Steps

The dataset will be cleaned, validated and transformed during the ETL phase before integration with crime and geographic datasets for downstream analytics.