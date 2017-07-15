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

Also, you probably want to specify what accounts, pages, subreddits to scrape!

So in the top level directory you should include all the above information in a
file named `config.py`, which should look like this:
```
TWITTER = {                                                                     
    'CONSUMER_KEY': 'xxxxxxxx',                                
    'CONSUMER_SECRET': 'xxxxxxx',    
    'ACCESS_TOKEN': 'xxxxxxxxxxx',       
    'ACCESS_SECRET': 'xxxxxxxxxx',           
}                                                                               
FACEBOOK = {                                                                    
    'APP_ID': 'xxxxxxxxxxxxxxx',                                               
    'APP_SECRET': 'xxxxxxxxxxxx',                           
}                                                                               
REDDIT = {                                                                      
    'CLIENT_ID': 'xxxxxxxxxxxx',                                              
    'CLIENT_SECRET': 'xxxxxxxxxxxxxxx',                             
    'USER_AGENT': 'User-Agent: web:com.xxxxxxx.xxxxxx:v1.0 (by /u/xxxxxxxx)',
}                                                                               
                                                                                
twitterUsernames = [                                                            
    'screen_name'                                                                   
]                     
fbPages = [                                                                     
    'page'                                                                  
]                                                                               
subreddits = [                                                                  
    'subreddit'                                                                
]               
```

To spin up your own version of quorum you can run the following command at the
top level directory of this project:
```
./start.sh
```

# Working on the documentation :-)
