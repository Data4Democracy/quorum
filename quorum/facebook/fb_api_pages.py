import os
import sys
import json
import requests
from time import sleep
from kafka import KafkaProducer, KafkaConsumer
import facepy
import facebook
from config import FACEBOOK



def format_post(post):       
    if isinstance(post['link'],list):
        links = ','.join(post['link'])
    elif isinstance(post['link'],str):
        links = post['link']
    else:
        links = ''
  
    formatedPost = {                                                           
        'idstr': post['id'],                                                  
        'created_at': post['created_time'],                                      
        'author': post['from']['name'],                                 
        'text': post['message'],                                                  
        'urls': links,                           
        'platform': 'facebook',
    }                                                                           
    return formatedPost 


def authenticate_api():
    auth_token = facepy.utils.get_application_access_token(FACEBOOK['APP_ID'], 
                                                           FACEBOOK['APP_SECRET'],
                                                           api_version='2.9')
    graph = facebook.GraphAPI(auth_token)
    return graph


def get_page_posts(page):
    # Connect to Kafka
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    # Facebook API
    graph = authenticate_api()

    all_fields = [                                                              
        'id',
        'created_time',
        'from',
        'message', 
        'link',
    ] 
    all_fields = ','.join(all_fields) 
    posts = graph.get_connections(page, 'posts', fields=all_fields)
    total_posts = 0                                                             
    need_update = True                 
    while True:                                                
        if total_posts >= 1000:                                                
            break                                                               
        try:                                                                                                             
            for post in posts['data']:
                msg = producer.send('data', json.dumps(format_post(post)).encode('utf-8'))
                total_posts += 1                                             
                print(total_posts)
                with open('test.jsonl', 'a') as f: 
                    f.write(json.dumps(format_post(post))+'\n')   

            # Flush kafka producer                                              
            producer.flush()
            # get next page                                                 
            posts = requests.get(posts['paging']['next']).json()            
        except KeyError:                                                        
            # no more pages, break the loop   
            print('No more posts...')
            break      
        except Exception as e:
            print(e)
            sleep(15*60)
            break

    # Flush kafka producer                                              
    producer.flush()
    return page


if __name__=="__main__":
    dev = os.environ.get('DEVELOPMENT') 
    if dev:
        get_page_posts('PacktPub')
    else:
        consumer = KafkaConsumer('fbPage', bootstrap_servers=['kafka:9092'])
        for msg in consumer:
            with open('test.txt', 'a') as f:
                f.write(msg.value.decode('utf-8')+'\n')
            get_page_posts(msg.value.decode('utf-8'))

