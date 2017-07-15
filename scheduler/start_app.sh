#!/bin/bash

export PS4='$(tput setaf 1)$(tput setab 7) + $(tput sgr 0)'                     
clear                                               
set -x  

sudo rm -f test*                                                                
sudo rm -rf data/
sudo docker-compose down --remove-orphans --volumes                             
sudo docker-compose -f $dockercomposefile up --build -d 

set +x
sleep 15
set -x
sudo docker-compose ps && sudo docker ps
