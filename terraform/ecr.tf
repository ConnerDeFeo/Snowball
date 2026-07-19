locals {
    repositories = ["orchestrator", "analysis-pipeline", "review-pipeline"]
}

# Add repositories for oeach of the repos
resource "aws_ecr_repository" "snowball" {
  for_each             = toset(local.repositories)
  name                 = "snowball/${each.value}"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# Remove non-latest images
resource "aws_ecr_lifecycle_policy" "cleanup" {
  for_each   = aws_ecr_repository.snowball
  repository = each.value.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep only the last 3 tagged images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 3
        }
      action = { type = "expire" }
    }]
  })
}

output "repository_urls" {
  value = { for k, repo in aws_ecr_repository.snowball : k => repo.repository_url }
}