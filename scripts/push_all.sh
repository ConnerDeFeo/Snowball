#!/bin/bash
set -e
 
# List of "dir:image_name:repo_name" entries to build and push.
# dir        = path (relative to project root) containing the Dockerfile
# image_name = local tag to build the image as
# repo_name  = the ECR repo suffix (snowball/<repo_name>)
images=(
    "orchestrator:orchestrator:orchestrator"
    "analysis-pipeline:analysis-pipeline:analysis-pipeline"
    "review-pipeline:review-pipeline:review-pipeline"
)
 
project_root=".."
 
for entry in "${images[@]}"; do
    dir="$(echo "$entry" | cut -d: -f1)"
    image_name="$(echo "$entry" | cut -d: -f2)"
    repo_name="$(echo "$entry" | cut -d: -f3)"
 
    echo "Building $image_name from $project_root/$dir"
    docker build -t "$image_name:latest" "$project_root/$dir"
 
    echo "Pushing $image_name -> snowball/$repo_name"
    ./push_ecr.sh "$image_name" "$repo_name"
done