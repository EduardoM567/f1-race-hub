#!/bin/bash

#mg792 - update system packages
sudo apt update -y

#mg792 - instal PHP and required extensions
sudo apt install -y php php-cli php-mbstring unzip curl git openssh-server rabbitmq-server

#mg792 - ensure RabbitMQ server is installed and running
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

#mg792 - install composer
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer

composer install

#mg792 - show completion 
echo "Setup complete"
