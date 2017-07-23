import os
import sys
import json
from time import sleep
from kafka import KafkaProducer, KafkaConsumer
from tweepy import API, OAuthHandler, Cursor, TweepError
from config import TWITTER



def format_tweet(tweet):    
    urls = ','.join( url['expanded_url'] for url in tweet['entities']['urls'] )
    
    formatedTweet = {                                                           
        'idstr': tweet['id_str'],                                                  
        'created_at': tweet['created_at'],                                      
        'author': tweet['user']['screen_name'],                                 
        'text': tweet['text'],                                                  
        'urls': urls,  
        'platform': 'twitter',
    }
    return formatedTweet 


def authenticate_api():
    auth = OAuthHandler(TWITTER["CONSUMER_KEY"], TWITTER["CONSUMER_SECRET"])
    auth.set_access_token(TWITTER["ACCESS_TOKEN"], TWITTER["ACCESS_SECRET"])
    api = API(auth, wait_on_rate_limit=True, 
              wait_on_rate_limit_notify=True,
              compression=True)                                             
    return api


def get_user_tweets(username):
    # Connect to Kafka
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    # Twitter API
    api = authenticate_api()

    tweets = 0
    need_update = True
    try:
        for page in Cursor(api.user_timeline, screen_name=username, count=200).pages(16):
            for status in page:
                status = status._json
                msg = producer.send('data', json.dumps(format_tweet(status)).encode('utf-8'))
                tweets += 1
                print(tweets)

                with open('test1.jsonl', 'a') as f:
                    f.write(json.dumps(format_tweet(status))+'\n')
            
            # Flush kafka producer
            producer.flush()      
            # Follow Twitter's Rate limit 
            sleep(2)
    except Exception as e:
        print(e)
        pass

    # Flush kafka producer                                              
    producer.flush()
    return username


if __name__=="__main__":
    dev = os.environ.get('DEVELOPMENT')
    if dev:
        get_user_tweets('gcosma1')
    else:
        consumer = KafkaConsumer('twitterUser', bootstrap_servers=['kafka:9092'])
        for msg in consumer:
            with open('test.txt', 'a') as f:
                f.write(msg.value.decode('utf-8')+'\n')
            get_user_tweets(msg.value.decode('utf-8'))
