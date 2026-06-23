#!/bin/bash
# API VM Setup Script
# Owner: Eduardo (em567)
# Role: API VM
# Description: Installs minimum required software for the API VM role

set -e

echo "Starting API VM setup..."

# Update package list
sudo apt-get update -y

# Install Python3 and pip if not already installed
if ! command -v python3 &> /dev/null; then
    echo "Installing Python3..."
    sudo apt-get install -y python3 python3-pip
else
    echo "Python3 already installed: $(python3 --version)"
fi

# Install pika for RabbitMQ communication
if ! dpkg -l | grep -q python3-pika; then
    echo "Installing pika..."
    sudo apt-get install -y python3-pika
else
    echo "pika already installed"
fi

echo "API VM setup complete!"
