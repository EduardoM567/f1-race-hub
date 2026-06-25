#!/bin/bash
#DB Setup Script
#Owner: Branden (bb449)
#Role: DB vm
#Description: Installs minimum software required for database vm role.

set e

echo "Starting DB vm setup ..."

#update package list
sudo apt update
sudo apt upgrade

#Install iputils
sudo apt install iputils-ping

#Install mySQL
sudo apt install mysql-server 

echo "DB vm is complete"