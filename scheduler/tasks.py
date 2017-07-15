from kafka import KafkaProducer, KafkaConsumer
import pytz
import datetime
import json                                                                     
import sqlalchemy                                                               
from sqlalchemy.sql import select                                               
from sqlalchemy import Column, Integer, Text, String                            
from sqlalchemy.dialects.postgresql import JSON, JSONB


def get_user_tweets(username):
    print("User: ", username)
    """
    producer = KafkaProducer(bootstrap_servers='kafka:9092') 
    consumer = KafkaConsumer('twitterCheckpoint', bootstrap_servers=['kafka:9092']) 
    msgSent = producer.send('twitterUser', username.encode('utf-8'))

    # wait for msg to be send back by producer
    msgReceived = None
    while not msgReceived:
        for msg in consumer:
            msgReceived = msg.value.decode('utf-8')

            if msgReceived==username:
                return
    """

def get_page_posts(page):                                                       
    print("Page: ", page)
    """
    producer = KafkaProducer(bootstrap_servers='kafka:9092')                    
    consumer = KafkaConsumer('fbCheckpoint', bootstrap_servers=['kafka:9092'])                                                                              
    msgSent = producer.send('fbPage', page.encode('utf-8'))                 

    # wait for msg to be send back by producer
    msgReceived = None                        
    while not msgReceived:                                                      
        for msg in consumer:                                                    
            msgReceived = msg.value.decode('utf-8')                             
                                                                                
            if msgReceived==page:                                               
                return                                                          
    """ 

def get_subreddit_posts(subr):                                                  
    print("subreddit: ", subr)
    """
    producer = KafkaProducer(bootstrap_servers='kafka:9092')                    
    consumer = KafkaConsumer('redditCheckpoint', bootstrap_servers=['kafka:9092'])                                                                            
    msgSent = producer.send('subreddit', subr.encode('utf-8'))                  

    # wait for msg to be send back by producer
    msgReceived = None                                                          
    while not msgReceived:                                                      
        for msg in consumer:                                                    
            msgReceived = msg.value.decode('utf-8')                             
                                                                                
            if msgReceived==subr:                                               
                return  
    """

def add_users(user, tablename):
    """ add a 'user' entry to a DB.

    Params
    ------
    user : str 
        It can be a twitter handle, a fb page, or a subreddit
    tablename: str
        name of db table to write to
    """
    # Connect to postgres DB 
    connection_string = 'postgresql://user:pass@usersdb/usersdb'
    db = sqlalchemy.create_engine(connection_string)                                
    engine = db.connect()                                                           
    meta = sqlalchemy.MetaData(engine)                                              
    meta.reflect(bind=engine)

    # Manage tables
    try:                                                                            
        table = sqlalchemy.Table(tablename,                                    
                                 meta,                                              
                                 Column('screen_name', Text, primary_key=True),     
                                 Column('last_scraped', Text),                      
                                 extend_existing=True)                              
        table.create(engine)                                                        
    except sqlalchemy.exc.ProgrammingError as e:                                    
        print("Table already existis")                                              
        pass         

    # Insert data
    try:                                                                                
        record = sqlalchemy.table(tablename,                                   
                                  Column('screen_name', Text),                      
                                  Column('last_scraped', Text))                     
        statement = record.insert().values(                                         
            screen_name = user,                                                 
            last_scraped = '',                                                 
        )                                                                           
        engine.execute(statement)                                                   
    except sqlalchemy.exc.IntegrityError as e:
        print("User already exists in db.")

    return


def scrape_users(tablename):
    """  
    """
    # Connect to postgres DB
    connection_string = 'postgresql://user:pass@usersdb/usersdb' 
    db = sqlalchemy.create_engine(connection_string)
    engine = db.connect() 
    meta = sqlalchemy.MetaData(engine)  
    meta.reflect(bind=engine) 

    # Manage tables
    table = meta.tables[tablename]

    # Update data
    runs = 0
    rows = engine.execute(select([table.c.screen_name]))
    for row in rows.fetchall():
        username = row[0]
        if tablename=='twitterusers':
            get_user_tweets(username)
        elif tablename=='fbpages':
            get_page_posts(username) 
        elif tablename=='subreddits':
            get_subreddit_posts(username)
        
        # update `last scrpaed` time
        now = datetime.datetime.now(pytz.utc)
        update = table.update().values(
            last_scraped=now.strftime("%Y-%m-%d %X %Z")
        ).where(table.c.screen_name==username)
        engine.execute(update)
        
        runs += 1

    with open('test.txt', 'a') as f:
        f.write('scraped {} for {}\n'.format(runs, tablename))
    print("scraped {} for {}".format(runs, tablename))

