# Cloud Data Lake Architecture

## AWS Region

eu-west-2 (London)

## Bucket

uk-housing-intelligence-platform-datalake-883627150629

## Layers

### Bronze

Raw source data

- Land Registry
- Crime Data
- Earnings Data
- Postcode Data
- Reference Data

### Silver

Cleaned and standardized datasets

- Property Prices
- Crime Clean
- Postcode Clean
- Housing Master Dataset
- Future Enrichment Datasets

### Gold

Business-ready analytics datasets

- Affordability Scores
- Crime Scores
- Growth Scores
- Investment Scores
- Housing Intelligence Index

## Security

- Versioning Enabled
- SSE-S3 Encryption Enabled
- Public Access Blocked

## Future Components

- AWS Glue Data Catalog
- Amazon Athena
- Terraform
- GitHub Actions

## S3 Structure

```text
s3://uk-housing-intelligence-platform-datalake-883627150629

bronze/
├── land_registry/
├── crime/
├── earnings/
├── postcode/
└── reference/

silver/
├── property_prices/
├── crime_clean/
├── postcode_clean/
├── housing_master/
└── enrichment/

gold/
├── affordability/
├── crime_scores/
├── growth/
├── investment/
└── housing_index/
```