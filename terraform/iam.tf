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

resource "aws_iam_role_policy" "ec2_dynamodb" {
  for_each = {
    documents         = aws_dynamodb_table.snowball_documents.arn
    findings          = aws_dynamodb_table.snowball_findings.arn
    section_grades    = aws_dynamodb_table.snowball_section_grades.arn
    rubric_directions = aws_dynamodb_table.snowball_rubric_directions.arn
  }

  name = "snowball-ec2-dynamodb-${replace(each.key, "_", "-")}"
  role = aws_iam_role.snowball_iam.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query",
      ]
      Resource = each.value
    }]
  })
}
