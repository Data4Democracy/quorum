#!/bin/bash

export PS4='$(tput setaf 1)$(tput setab 7) + $(tput sgr 0)'
clear
set -x


sudo docker-compose down --remove-orphans --volumes
sudo docker-compose up --build -d

set +x
echo -e "$(tput setaf 1)\tCreate multiple Kafka Topics for Communication between containers...$(tput sgr 0)"
sudo docker-compose exec kafka /bin/bash -c "\
    bin/kafka-topics.sh --list --zookeeper zookeeper:2181 && \
    bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic twitterUser       && \
    bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic twitterCheckpoint && \
    bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic fbPage            && \
    bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic fbCheckpoint      && \
    bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic subreddit         && \
    bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic redditCheckpoint  && \
    bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic data              && \
    bin/kafka-topics.sh --list --zookeeper zookeeper:2181 && \
    exit"
sleep 5
echo -e "$(tput setaf 1)\tMaking sure services were spun up properly...$(tput sgr 0)"
set -x
sudo docker-compose ps && sudo docker ps
