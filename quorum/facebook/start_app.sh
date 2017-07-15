#!/bin/bash

export PS4='$(tput setaf 1)$(tput setab 7) + $(tput sgr 0)'                     
set -x  

rm -f test*                                                                
docker-compose down --remove-orphans --volumes                             
docker-compose up --build -d

set +x
sleep 5
set -x
docker-compose ps && docker ps
