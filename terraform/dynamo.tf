resource "aws_dynamodb_table" "snowball_documents" {
  name         = "snowball_documents"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "accession"

  attribute {
    name = "accession"
    type = "S"
  }
}

resource "aws_dynamodb_table" "snowball_checklist" {
  name         = "snowball_checklist"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "category_id"
  range_key    = "sk"

  attribute {
    name = "category_id"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }
}

resource "aws_dynamodb_table" "snowball_evidence" {
  name         = "snowball_evidence"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "tckr"
  range_key    = "evidence_key"

  attribute {
    name = "tckr"
    type = "S"
  }

  attribute {
    name = "evidence_key"
    type = "S"
  }
}

resource "aws_dynamodb_table" "snowball_companies" {
  name         = "snowball_companies"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "tckr"

  attribute {
    name = "tckr"
    type = "S"
  }
}

resource "aws_dynamodb_table" "snowball_review_sessions" {
  name         = "snowball_review_sessions"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "session_id"

  attribute {
    name = "session_id"
    type = "S"
  }

  ttl {
    attribute_name = "expires_at"
    enabled        = true
  }
}

