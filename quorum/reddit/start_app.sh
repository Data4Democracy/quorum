#!/bin/bash

export PS4='$(tput setaf 1)$(tput setab 7) + $(tput sgr 0)'                     
clear                                                                           

dockercomposefile="docker-compose.yml"                                          
if [ $DEVELOPMENT ]; then                                                       
    dockercomposefile="docker-compose_dev.yml"                                  
fi 

set -x 

sudo rm -r data
sudo rm -f test*
sudo docker-compose down --remove-orphans                                       
sudo docker-compose -f $dockercomposefile up --build -d

set +x
sleep 5
set -x
sudo docker-compose ps && sudo docker ps
