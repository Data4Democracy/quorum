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
First off, the scrapers are implemented using the official APIs for each
platform. As such, in order to use you will need the proper credentials.

Also, you need  to specify what accounts, pages, subreddits to scrape!

In the top level directory run the command below.

```
  $ cp config_example.py config.py

```

Edit the config.py with the needed service credentials.

To spin up your own version of quorum you can run the following command at the
top level directory of this project:
```
./start.sh
```

#Tests

```
$ python -m unittest discover quorum/facebook
```

Todo: add a way to read all the tests in all the folders with one script or command. Will also
need to install dependencies before hand to get this to work. 
# Working on the documentation :-)
