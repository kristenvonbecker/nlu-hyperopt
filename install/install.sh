#!/bin/bash
set -Eeuo pipefail

#######################################
#
# installing ansible and roles
#
#######################################
echo "Installing Ansible"
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible

echo "Installing Docker role and dependencies"
sudo apt-get install libssl-dev libcurl4-openssl-dev python3.8-dev
ansible-galaxy install angstwad.docker_ubuntu
echo "Docker installed"

#######################################
#
# running the ansible playbook
# (starts docker und serves platform)
#
#######################################
echo "Running playbook"
ansible-playbook -i "localhost," -c local install/playbook.yml
