import json
import sqlalchemy  
from time import sleep
from kafka import KafkaProducer, KafkaConsumer 
from sqlalchemy import Column, Integer, Text  
from sqlalchemy.dialects.postgresql import JSON, JSONB


def data_to_db():
    db = sqlalchemy.create_engine('postgresql://user:pass@postgres/mydatabase')
    engine = db.connect()  
    meta = sqlalchemy.MetaData(engine) 

    sqlalchemy.Table("jsontable", meta,  
                     Column('idstr', Text, Text, primary_key=True),
                     Column('created_at', Text),
                     Column('author', Text),
                     Column('text', Text),
                     Column('urls', Text),
                     Column('platform', Text))
    meta.create_all()
    j_table = sqlalchemy.table("jsontable",
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
        for k,v in msg.items():
            if isinstance(v,(int,float)):
                msg[k] = str(v)
            if isinstance(v, str):
                msg[k] = ''.join([i if ord(i) < 128 else ' ' for i in v])
        try:
            statement = j_table.insert().values(idstr=msg['idstr'],
                                                created_at=msg['created_at'],
                                                author=msg['author'],
                                                text=msg['text'],
                                                urls=msg['urls'],
                                                platform=msg['platform'])
            engine.execute(statement)

            records += 1
            with open('test.txt','a') as f:
                f.write(json.dumps(msg)+'\n')
            print(records)
        except Exception as e:    
            print(e)                                                            
            continue     

        if records%100==0:
            print(records)

    return records

if __name__=="__main__":
    sleep(10)
    data_to_db()
