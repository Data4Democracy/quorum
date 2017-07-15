#!/bin/bash

# Docker Installation in Ubuntu/Xenial 16.04


# Unistall old versions
sudo apt-get remove -y docker docker-engine

# Install packages to allow apt to use a repository over HTTPS:
sudo apt-get update -y && sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common 

# Add Docker’s official GPG key:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sleep 5
echo "Verify that the key fingerprint is:\t\n 9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88\n"
sleep 5

sudo apt-key fingerprint 0EBFCD88

# set up a stable repo
sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"


# Install docker
sudo apt-get update -y && sudo apt-get install -y docker-ce

# Get Docker version
apt-cache madison docker-ce


# Test it
sudo docker run --rm hello-world

# Install docker-compose
sudo curl -o /usr/local/bin/docker-compose -L "https://github.com/docker/compose/releases/download/1.13.0/docker-compose-$(uname -s)-$(uname -m)"

sudo chmod +x /usr/local/bin/docker-compose

docker-compose -v

