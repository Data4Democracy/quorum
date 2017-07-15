import tasks
import time
import schedule


def job():
    print("I'm working...")


def add_users_to_db(db_uri='postgresql://user:pass@usersdb/usersdb'):
    import config

    # add each entry to DB
    for entry in config.twitterUsernames:
        tasks.add_users(entry, 'twitterusers', db_uri=db_uri)

    for entry in config.fbPages:
        tasks.add_users(entry, 'fbpages', db_uri=db_uri)
   
    for entry in config.subreddits:
        tasks.add_users(entry, 'subreddits', db_uri=db_uri)

    with open('test.txt', 'a') as f:
        f.write("All users have been added to DB\n")
    print("All users have been added to DB")


if __name__=="__main__":

    # DB
    db_uri='postgresql://user:pass@usersdb/usersdb'


    # TASKS
    schedule.every(1).minutes.do(job)
    
    # update DB with accounts to scrape
    schedule.every(1).minutes.do(add_users_to_db)

    # scrape all accounts for given DB table
    schedule.every(1).minute.do(tasks.scrape_users, tablename='twitterusers', db_uri=db_uri)
    schedule.every(1).minute.do(tasks.scrape_users, tablename='fbpages',      db_uri=db_uri)
    schedule.every(1).minute.do(tasks.scrape_users, tablename='subreddits',   db_uri=db_uri)


    while True:
        schedule.run_pending()
        time.sleep(5)
        
