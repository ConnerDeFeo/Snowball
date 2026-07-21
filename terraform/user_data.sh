#!/bin/bash
set -ex

# Git + Docker
dnf install -y git docker
systemctl enable --now docker
usermod -aG docker ec2-user

# Node/npm + wscat
dnf install -y nodejs
npm install -g wscat

# Docker Compose CLI plugin
DOCKER_CONFIG=/usr/local/lib/docker
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
  -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

# Clone repo
cd /home/ec2-user
sudo -u ec2-user git clone https://github.com/ConnerDeFeo/Snowball.git
cd Snowball

# Secrets
sudo -u ec2-user mkdir -p secrets
sudo -u ec2-user cp secrets.example/EDGAR_IDENTITY.txt secrets/EDGAR_IDENTITY.txt

# ECR login
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 857360184083.dkr.ecr.us-east-2.amazonaws.com

# Boot the prod stack
docker compose -f docker-compose.prod.yml up -d
