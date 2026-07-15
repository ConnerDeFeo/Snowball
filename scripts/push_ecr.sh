#!/bin/bash
tag=$(git rev-parse --short HEAD)
image_name=$1 
repo_name=$2

docker tag "$image_name:latest" "857360184083.dkr.ecr.us-east-2.amazonaws.com/snowball/$repo_name:$tag"
docker push "857360184083.dkr.ecr.us-east-2.amazonaws.com/snowball/$repo_name:$tag"

echo "Image Tag: $tag"
