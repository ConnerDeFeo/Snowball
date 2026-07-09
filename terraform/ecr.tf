# Login for ecr (powershell)
# cmd /c "aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 857360184083.dkr.ecr.us-east-2.amazonaws.com"
locals {
    registries = ["orchestrator", "analysis-pipeline", "review-pipeline"]
}

resource "aws_ecr_repository" "snowball" {
  for_each             = toset(local.registries)
  name                 = "snowball/${each.value}"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "repository_urls" {
  value = { for k, repo in aws_ecr_repository.snowball : k => repo.repository_url }
}