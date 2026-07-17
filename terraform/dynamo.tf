resource "aws_dynamodb_table" "snowball_documents" {
  name         = "snowball-documents"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "accession"

  attribute {
    name = "accession"
    type = "S"
  }
}
