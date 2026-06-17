# Terraform Infrastructure

## Overview

Terraform is used to manage AWS infrastructure through Infrastructure as Code.

Phase 7 imports existing AWS resources into Terraform state and manages them declaratively.

---

## Managed Resources

### S3

- Data Lake Bucket
- Athena Results Bucket

### IAM

- UKHousingGlueRole

### Glue

- uk_housing_intelligence Database
- Silver Layer Crawlers
- Gold Layer Crawlers

---

## Benefits

- Reproducibility
- Version Control
- Auditability
- Infrastructure Consistency
- Enterprise Cloud Engineering Practices