#!/bin/bash
set -e
 
# List of "dir:image_name:repo_name" entries to build and push.
# dir        = path (relative to project root) containing the Dockerfile
# image_name = local tag to build the image as
# repo_name  = the ECR repo suffix (snowball/<repo_name>)
images=(
    "orchestrator"
    "analysis-pipeline"
    "review-pipeline"
)
 
project_root=".."
 
for repo_name in "${images[@]}"; do
    ./scripts/push_ecr.sh "$repo_name"
done