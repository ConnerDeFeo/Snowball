### Login for ecr (powershell)
cmd /c "aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin (account_id).dkr.ecr.us-east-2.amazonaws.com"
---
### Push Docker Images to Ecr
docker tag (docker_image):latest (account_id).dkr.ecr.us-east-2.amazonaws.com/snowball/(docker_image):latest
docker push (account_id).dkr.ecr.us-east-2.amazonaws.com/snowball/(docker_image):latest