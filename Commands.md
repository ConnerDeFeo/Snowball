### Login for ecr (powershell)
cmd /c "aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 857360184083.dkr.ecr.us-east-2.amazonaws.com"

### Login for ECR (AML)
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 857360184083.dkr.ecr.us-east-2.amazonaws.com
---

### Push Docker Images to ECR
$tag = git rev-parse --short HEAD
docker tag (DockerImage):latest 857360184083.dkr.ecr.us-east-2.amazonaws.com/snowball/(DockerImage):$tag
docker push 857360184083.dkr.ecr.us-east-2.amazonaws.com/snowball/(DockerImage):$tag

### Pull Docker Image from ECR
docker pull 857360184083.dkr.ecr.us-east-2.amazonaws.com/snowball/(DockerImage):<tag>

### Run Docker Images (AML)
