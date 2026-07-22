#!/usr/bin/env bash
# One-time provisioning of an env app box (Ubuntu 24.04)
set -euo pipefail
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update -y && sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin certbot
sudo usermod -aG docker ubuntu
sudo mkdir -p /opt/healthekit/{env,nginx}
echo "Copy docker-compose.<env>.yml, nginx/<env>.conf and env/.env.<env>; then: certbot certonly --standalone -d api.<env>.healthekit.in -d <env>.healthekit.in"
