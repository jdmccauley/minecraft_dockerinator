#!/bin/bash

# Source: Docker's guide on installing Docker on Ubuntu
# https://docs.docker.com/engine/install/ubuntu/

# The purpose of this script is to automate the installation of Docker on a new Ubuntu server
# Assumes CPU architecture is x86_64 or amd64
# This should be run as root or sudoer

# Uninstall older versions of docker
apt-get remove docker docker-engine docker.io containerd runc

# Update and install dependencies
apt-get update
apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

# Add Docker gpg key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Verify fingerprint
apt-key fingerprint 0EBFCD88

# Get Docker
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# Install Docker Engine
apt-get update
apt-get install docker-ce docker-ce-cli containerd.io
