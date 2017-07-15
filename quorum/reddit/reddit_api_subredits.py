import os
import sys
import json
from time import sleep
from kafka import KafkaProducer, KafkaConsumer
import praw
from config import REDDIT



def format_submission(submission):                                                        
    formatedSub = {                                                           
        'id': submission.id,                                                  
        'created_at': submission.created,                                      
        'author': submission.author,                                 
        'text': submission.title,                                                  
        'urls': submission.permalink,                           
        'platform': 'reddit',
    }
    for k,v in formatedSub.items():
        formatedSub[k] = str(v)

    return formatedSub 


def authenticate_api():
    reddit = praw.Reddit(client_id=REDDIT['CLIENT_ID'],
                         client_secret=REDDIT['CLIENT_SECRET'],
                         user_agent=REDDIT['USER_AGENT'])
    return reddit


def get_reddit_submissions(subreddit):
    # Connect to Kafka
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    # Reddit API
    reddit = authenticate_api()

    submissions = 0
    need_update = True
    try:
        for submission in reddit.subreddit(subreddit).new():
            sub = format_submission(submission)
            if submissions > 1000:
                break
     
            msg = producer.send('data', json.dumps(sub).encode('utf-8'))
            submissions += 1
            print(submissions)
            with open('test.jsonl', 'a') as f:
                f.write(json.dumps(sub)+'\n') 

        # Flush kafka producer
        producer.flush()
    except Exception as e:
        with open('Errors.txt', 'a') as f:
            f.write(str(e)+'\n') 
        print(e)
        print('Taking a short nap...')
        sleep(15*60)

    # Flush kafka producer                                                  
    producer.flush()
    return subreddit


if __name__=="__main__":
    sleep(10)
    dev = os.environ.get('DEVELOPMENT')
    if dev:
        get_reddit_submissions('AskReddit')
    else:
        consumer = KafkaConsumer('subreddit', bootstrap_servers=['kafka:9092'])
        for msg in consumer:
            with open('test.txt', 'a') as f:
                f.write(msg.value.decode('utf-8')+'\n')
            get_reddit_submissions(msg.value.decode('utf-8'))
