#!/bin/bash
sudo apt update -y
sudo apt install -y php php-cli unzip git composer rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
sudo rabbitmqctl add_user it490 it490pass
sudo rabbitmqctl set_permissions -p / it490 ".*" ".*" ".*"

