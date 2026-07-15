### Push Docker Images to ECR
tag=$(git rev-parse --short HEAD)
docker tag (DockerImage):latest 857360184083.dkr.ecr.us-east-2.amazonaws.com/snowball/(DockerImage):$tag
docker push 857360184083.dkr.ecr.us-east-2.amazonaws.com/snowball/(DockerImage):$tag

### Pull Docker Image from ECR
docker pull 857360184083.dkr.ecr.us-east-2.amazonaws.com/snowball/(DockerImage):<tag>
