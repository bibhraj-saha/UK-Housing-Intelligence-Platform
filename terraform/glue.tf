resource "aws_glue_catalog_database" "housing_db" {
  name        = "uk_housing_intelligence"
  description = "UK Housing Intelligence Platform Data Catalog"
}

resource "aws_glue_crawler" "crime_clean" {
  name          = "crime-clean-crawler"
  database_name = aws_glue_catalog_database.housing_db.name
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://uk-housing-intelligence-platform-datalake-883627150629/silver/crime_clean/"
  }
}

resource "aws_glue_crawler" "housing_master" {
  name          = "housing-master-crawler"
  database_name = aws_glue_catalog_database.housing_db.name
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://uk-housing-intelligence-platform-datalake-883627150629/silver/housing_master/"
  }
}

resource "aws_glue_crawler" "postcode_clean" {
  name          = "postcode-clean-crawler"
  database_name = aws_glue_catalog_database.housing_db.name
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://uk-housing-intelligence-platform-datalake-883627150629/silver/postcode_clean/"
  }
}

resource "aws_glue_crawler" "property_geography" {
  name          = "property-geography-crawler"
  database_name = aws_glue_catalog_database.housing_db.name
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://uk-housing-intelligence-platform-datalake-883627150629/silver/property_geography/"
  }
}

resource "aws_glue_crawler" "property_prices" {
  name          = "property-prices-crawler"
  database_name = aws_glue_catalog_database.housing_db.name
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://uk-housing-intelligence-platform-datalake-883627150629/silver/property_prices/"
  }
}

resource "aws_glue_crawler" "gold_intelligence" {
  name          = "gold-intelligence-crawler"
  database_name = aws_glue_catalog_database.housing_db.name
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://uk-housing-intelligence-platform-datalake-883627150629/gold/"
  }
}

resource "aws_glue_crawler" "gold_trends" {
  name          = "gold-trends-crawler"
  database_name = aws_glue_catalog_database.housing_db.name
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://uk-housing-intelligence-platform-datalake-883627150629/gold/trends/"
  }
}