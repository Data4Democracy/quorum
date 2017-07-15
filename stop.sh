#!/bin/bash

NORMAL="\\033[0;39m"                                                            
RED="\\033[1;31m"                                                               
BLUE="\\033[1;34m"                                                              
                                                                                
logs=$(pwd)                                                                     
                                                                                
log() {                                                                         
    echo -e "$BLUE > $1 $NORMAL"                                                   
}                                                                               
                                                                                
error() {                                                                       
    echo ""                                                                     
    echo -e "$RED >>> ERROR - $1$NORMAL"                                           
}                                                                               
export PS4='$(tput setaf 1)$(tput setab 7) + $(tput sgr 0)'                     
clear                                                                           

log "Taking everything down first..."
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

