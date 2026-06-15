#!/bin/bash
sudo apt update
sudo apt upgrade
sudo apt install nano
sudo apt install iputils-ping
sudo apt install git
sudo apt install software-properties-common
sudo add-apt-repository ppa:ondrej/php
sudo apt update
sudo apt install php8.5
sudo apt install php8.5-intl php8.5-curl php8.5-mbstring php8.5-xml
sudo apt install composer
sudo apt install rabbitmq-server
git clone https://github.com/MattToegel/IT490-2026
cd IT490-2026
composer install
#rkp28
