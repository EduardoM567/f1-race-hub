#!/bin/bash
#rkp28 app script

sudo apt-get update -y

sudo apt-get upgrade -y

sudo apt-get install -y apache2
sudo apt-get install -y php8.3 php8.3-cli php8.3-curl php8.3-mbstring
sudo apt-get install -y composer
sudo apt-get install -y iputils-ping
sudo apt-get install -y nano


