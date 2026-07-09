locals {
    registries = ["orchestrator", "analysis-pipeline", "review-pipeline"]
}

resource "aws_ecr_repository" "snowball" {
  for_each             = toset(locals.registries)
  name                 = "snowball/${each.value}"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "repository_urls" {
  value = { for k, repo in aws_ecr_repository.snowball : k => repo.repository_url }
}