# Amazon Athena Analytics

## Overview

Amazon Athena provides serverless SQL analytics directly on datasets stored in Amazon S3.

No database servers are required.

Athena queries data registered in the AWS Glue Catalog.

---

## Example Queries

### Property Transactions

```sql
SELECT COUNT(*)
FROM property_prices;
```

### Average House Price

```sql
SELECT AVG(price)
FROM housing_master;
```

### Top Ranked Areas

```sql
SELECT *
FROM rankings
ORDER BY housing_intelligence_index DESC
LIMIT 10;
```

---

## Benefits

- Serverless
- Pay-per-query
- Fast analytics on Parquet files
- No infrastructure management
- Cloud-native SQL layer