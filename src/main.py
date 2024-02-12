import dbOps
import scrapOps
import requests
import creds
import mailOps
import time


def login_operation(username, password):
    # Login to mysu
    target_url = 'https://mysu.sabanciuniv.edu/announcements/en/all' #maybe I shouldn't hardcode this
    login_url = 'https://login.sabanciuniv.edu/cas/login?service=https%3A%2F%2Fmysu.sabanciuniv.edu%2Fannouncements%2Fen%2Fall'
    evid = 'submit'
    login_data = {'username': username, 'password': password, 'execution': creds.exec, '_eventId': evid}

    with requests.Session() as s:
        r = s.post(login_url, data=login_data)
        r = s.get(target_url)
        return r.text


def suduyuru():
    """the main function"""
    #it will be called by the scheduler
    
    #connect to the database
    db = dbOps.connect_to_database('root', 'example')

    #login to mysu
    html_txt = login_operation(creds.username, creds.password)

    #scrape the announcements
    duyuru_dict = scrapOps.scraper(html_txt)

    #insert the announcements into the database
    dbOps.insert_announcements(duyuru_dict, db)

    #send the email
    mailOps.send_mail(creds.email_address, creds.email_password, creds.email_server, creds.port, db)

    #manage old announcements
    dbOps.increment_ann_age(db)
    dbOps.wipe_old_announcements(db)


def main():
    #suduyuru will be run at 9 am on mondays, wednesdays and fridays

    #the problem is with the docker container time, that's why it worked on my system but not in the container
    #docker time set to UTC.
    print('hello, I am running.')
    while True:
        now = time.ctime().split(' ')
        days = ['Mon', 'Wed', 'Fri']

        if now[0] in days and now[3].split(':')[0] == '09':
            print('suduyuru is going to run, time: ', now[3])
            suduyuru()
            time.sleep(60*60)
        else:
            print('checked the time, suduyuru has not been run, time is: ',now[3])
            time.sleep(60*60)

if __name__ == "__main__":
    main()







