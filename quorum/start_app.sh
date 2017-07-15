#!/bin/bash

clear

set -o xtrace
sudo rm -r data
sudo docker-compose down --remove-orphans                                       
sudo docker-compose build && sudo docker-compose up -d 
