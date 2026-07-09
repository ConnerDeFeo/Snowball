### Login for ecr (powershell)
cmd /c "aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 857360184083.dkr.ecr.us-east-2.amazonaws.com"
---
### Push Docker Images to Ecr
docker tag (DockerImage):latest 857360184083.dkr.ecr.us-east-2.amazonaws.com/snowball/(DockerImage):latest
docker push 857360184083.dkr.ecr.us-east-2.amazonaws.com/snowball/(DockerImage):latest