resource "aws_dynamodb_table" "snowball_documents" {
  name         = "snowball_documents"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "accession"

  attribute {
    name = "accession"
    type = "S"
  }
}

resource "aws_iam_role_policy" "ec2_dynamodb_documents" {
  name = "snowball-ec2-dynamodb-documents"
  role = aws_iam_role.snowball_iam.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem",
        "dynamodb:Query",
        "dynamodb:Scan",
      ]
      Resource = aws_dynamodb_table.snowball_documents.arn
    }]
  })
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

resource "aws_iam_role_policy" "ec2_dynamodb_findings" {
  name = "snowball-ec2-dynamodb-findings"
  role = aws_iam_role.snowball_iam.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
      ]
      Resource = aws_dynamodb_table.snowball_findings.arn
    }]
  })
}
