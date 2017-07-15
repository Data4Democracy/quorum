import tasks
import time
import schedule


def job():
    print("I'm working...")


def add_users_to_db():
    import config

    # add each entry to DB
    for entry in config.twitterUsernames:
        tasks.add_users(entry, 'twitterusers')

    for entry in config.fbPages:
        tasks.add_users(entry, 'fbpages')
   
    for entry in config.subreddits:
        tasks.add_users(entry, 'subreddits')

    with open('test.txt', 'a') as f:
        f.write("All users have been added to DB\n")
    print("All users have been added to DB")


if __name__=="__main__":

    # TASKS
    schedule.every(1).minutes.do(job)
    # update DB with accounts to scrape
    schedule.every(1).minutes.do(add_users_to_db)
    # scrape all accounts for given DB table
    schedule.every(1).minute.do(tasks.scrape_users, tablename='twitterusers')
    schedule.every(1).minute.do(tasks.scrape_users, tablename='fbpages')
    schedule.every(1).minute.do(tasks.scrape_users, tablename='subreddits')


    while True:
        schedule.run_pending()
        time.sleep(5)
        
