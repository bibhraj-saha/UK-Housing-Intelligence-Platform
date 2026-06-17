resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-datalake-${var.account_id}"
}

resource "aws_s3_bucket" "athena_results" {
  bucket = "${var.project_name}-athena-results-${var.account_id}"
}