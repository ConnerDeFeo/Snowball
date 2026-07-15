#!/bin/bash
tag=$(git rev-parse --short HEAD)
repo_name=$1

echo "Building $repo_name"
docker build -t "$repo_name" "$repo_name/"

docker tag "$repo_name:latest" "857360184083.dkr.ecr.us-east-2.amazonaws.com/snowball/$repo_name:$tag"

echo "Pushing $repo_name -> snowball/$repo_name"
docker push "857360184083.dkr.ecr.us-east-2.amazonaws.com/snowball/$repo_name:$tag"

echo "Image Tag: $tag"
