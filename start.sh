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
clear                                                                           



if [ -e build.out ]; then 
    rm build.out
fi

if [ -e config.py ]; then
    cp config.py quorum/twitter/
    cp config.py quorum/facebook/
    cp config.py quorum/reddit/
else
    echo -e "$(tput setaf 1)\n\n\tNo config.py file found\n"
    echo -e "You need to have a \"config.py\" file that containes twitter/facebook/reddit credentials" 
    echo -e "and users/pages/subreddits to scrape.$(tput sgr 0)\n\n"
    exit 1
fi


# Stop all services
./stop.sh

# Start Kafka server
log "Kafka setup..."
cd kafka/
./setup_kafka.sh | tee ${logs}/build.out
cd ../

# Start DB
log "Postrges DB setup..."
cd storage/
./start_app.sh | tee -a ${logs}/build.out 
cd ../

# Start scrapers
log "Running scrapers..."
cd quorum/twitter/
./start_app.sh | tee -a ${logs}/build.out 
cd ../facebook/
./start_app.sh | tee -a ${logs}/build.out
cd ../reddit/
./start_app.sh | tee -a ${logs}/build.out
cd ../../

# Start queue
log "Starting scheduler..."
cd scheduler/
./start_app.sh | tee -a ${logs}/build.out 
cd ../
