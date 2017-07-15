#!/bin/bash

export PS4='$(tput setaf 1)$(tput setab 7) + $(tput sgr 0)'                     
clear                                                                           

export DEVELOPMENT=True
logs=$(pwd)

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

set -x

# Stop all services
./stop.sh

# Start Kafka server
cd kafka/
./setup_kafka.sh |& tee ${logs}/build.out
cd ../

# Start DB
cd storage/
./start_app.sh |& tee ${logs}/build.out 
cd ../

# Start scrapers
cd quorum/twitter/
./start_app.sh |& tee ${logs}/build.out 
cd ../facebook/
./start_app.sh |& tee ${logs}/build.out
cd ../reddit/
./start_app.sh |& tee ${logs}/build.out
cd ../../

# Start queue
cd scheduler/
./start_app.sh |& tee ${logs}/build.out 
../
