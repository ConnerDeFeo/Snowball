resource "aws_iam_role" "snowball_iam" {
  name = "snowball-ec2-s3-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "managed" {
  for_each = toset([
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
    "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore",
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
    "arn:aws:iam::aws:policy/AmazonBedrockFullAccess",
  ])
  role       = aws_iam_role.snowball_iam.name
  policy_arn = each.value
}

resource "aws_iam_instance_profile" "snowball_iam_profile" {
  name = "snowball-ec2-s3-profile"
  role = aws_iam_role.snowball_iam.name
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

resource "aws_iam_role_policy" "ec2_dynamodb_section_grades" {
  name = "snowball-ec2-dynamodb-section-grades"
  role = aws_iam_role.snowball_iam.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
      ]
      Resource = aws_dynamodb_table.snowball_section_grades.arn
    }]
  })
}
