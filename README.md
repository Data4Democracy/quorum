# Quorum
Your go-to ETL for online data

# Architecture
Quorum has four main different components:

1. **[Kafka](https://kafka.apache.org/):** An `Apache Kafka` server for streaming
  data to and from the other services.

2. **Scheduler:** A lightweght scheduler to plan and manage what to scrape and when
  to do it. Based on [schedule](https://github.com/dbader/schedule).

3. **storage:** Data `consumer` from a predefined `Kafka` topic and stores it in a
  persistent volume.

4. **quorum:** Content scrapers that produce to predefined `kafka topics`.
 Thus far we have incorporated the following scrapers:
    * Twitter
    * Facebook
    * Reddit


# Usage
To spin up your own version of quorum you can run the following command at the
top level directory of this project:
```
./start.sh
```

# Working on the documentation :-)
