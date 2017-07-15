#!/bin/bash


export PS4='$(tput setaf 1)$(tput setab 7) + $(tput sgr 0)'                     
clear                                                                           
set -x                                                                          
       
# Stop queue
cd scheduler/
docker-compose down
cd ../

# Stop scrapers
cd quorum/twitter
docker-compose down
cd ../facebook
docker-compose down
cd ../reddit
docker-compose down
cd ../../

# stop DB
cd storage
docker-compose down
cd ../

# Start Kafka server
cd kafka/
docker-compose down
cd ../

