#!/bin/bash


export PS4='$(tput setaf 1)$(tput setab 7) + $(tput sgr 0)'                     
clear                                                                           
set -x                                                                          
       
# Stop queue
cd celery/                                                                      
sudo docker-compose down                                        
cd ../

# Stop scrapers
cd quorum/twitter
sudo docker-compose down 
cd ../facebook
sudo docker-compose down
cd ../reddit
sudo docker-compose down
cd ../../

# stop DB
cd storage
sudo docker-compose down
cd ../

# Start Kafka server
cd kafka/
sudo docker-compose down 
cd ../

