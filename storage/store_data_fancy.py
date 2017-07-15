from time import sleep
from kafka import KafkaProducer, KafkaConsumer 
import json                                                                     
import sqlalchemy                                                               
from sqlalchemy.sql import select                                               
from sqlalchemy import Column, Integer, Text, String                            
from sqlalchemy.dialects.postgresql import JSON, JSONB  


def data_to_db():
    # Connect to DB
    db = sqlalchemy.create_engine('postgresql://user:pass@postgres/mydatabase')
    engine = db.connect()  
    meta = sqlalchemy.MetaData(engine) 
    meta.reflect(bind=engine)

    # Create/Extend table
    try:
        table = sqlalchemy.Table("jsontable", 
                                 meta,               
                                 Column('idstr', Text, primary_key=True),
                                 Column('created_at', Text),
                                 Column('author', Text),
                                 Column('text', Text),
                                 Column('urls', Text),
                                 Column('platform', Text),
                                 extend_existing=True)
        table.create(engine) 
    except sqlalchemy.exc.ProgrammingError as e:
        print("Table already existis")                                              
        pass

    # Upsert entry
    record = sqlalchemy.table("jsontable",
                              Column('idstr', Text),
                              Column('created_at', Text),
                              Column('author', Text), 
                              Column('text', Text),
                              Column('urls', Text),
                              Column('platform', Text))
    records = 0
    consumer = KafkaConsumer('data', bootstrap_servers=['kafka:9092'])
    for msg in consumer:                                                
        msg = json.loads(msg.value.decode('utf-8'))                                        
        # Get rid of any non-ascii chars
        for k,v in msg.items():
            if isinstance(v, str):
                msg[k] = ''.join([i if ord(i) < 128 else ' ' for i in v])

            # Insert row if not already existing
            try:
                statement = record.insert().values(idstr = msg['idstr'],
                                                   created_at = msg['created_at'],
                                                   author = msg['author'],
                                                   text = msg['text'],
                                                   urls = msg['urls'],
                                                   platform = msg['platform'])

                engine.execute(statement)
                records += 1
                with open('test.txt','a') as f:
                    f.write(json.dumps(msg)+'\n')
                print(records)
            except sqlalchemy.exc.IntegrityError as e:                                       
                continue     


    return records

if __name__=="__main__":
    sleep(10)
    data_to_db()
