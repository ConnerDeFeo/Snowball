resource "aws_dynamodb_table" "snowball_documents" {
  name         = "snowball_documents"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "accession"

  attribute {
    name = "accession"
    type = "S"
  }
}

resource "aws_dynamodb_table" "snowball_findings" {
  name         = "snowball_findings"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "section_key"
  range_key    = "version_key"

  attribute {
    name = "section_key"
    type = "S"
  }

  attribute {
    name = "version_key"
    type = "S"
  }
}

resource "aws_dynamodb_table" "snowball_section_grades" {
  name         = "snowball_section_grades"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "tckr"
  range_key    = "category_period"

  attribute {
    name = "tckr"
    type = "S"
  }

  attribute {
    name = "category_period"
    type = "S"
  }
}

