import dbOps
import scrapOps
import requests
import creds
import mailOps
import time
import clientOps

#config
import config

#logging setup
import logging

logging_level = config.log_lvl  #this sets the debugging level for the whole project
main_logger = logging.getLogger()
main_logger.setLevel(logging_level)

#stream handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging_level)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
stream_handler.setFormatter(formatter)

#add handler to logger
main_logger.addHandler(stream_handler)


def login_operation(username, password):
    # Login to mysu
    target_url = 'https://mysu.sabanciuniv.edu/announcements/en/all' #maybe I shouldn't hardcode this
    login_url = 'https://login.sabanciuniv.edu/CASV/LoginAction'
    evid = 'submit' #TODO: remove dead code
    login_data = {'ReturnUrl': '',
                  'LoginType': '',
                  'Email': username, 'Password': password,
                  'g-recaptcha-response': '',
                   '__RequestVerificationToken': creds.vertok,
                   }

    with requests.Session() as s:
        r = s.get(target_url, allow_redirects=True)
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
    mailOps.mail_process(creds.email_address, creds.email_password, creds.email_server, creds.port, db)

    #manage old announcements
    if(not config.testing):

        main_logger.debug("Testing mode is OFF, updating announcement age and wiping old announcements")

        dbOps.increment_ann_age(db)
        dbOps.wipe_old_announcements(db)

    else:
        main_logger.warning("Testing mode is ON, announcement ages not changed")


def main():

    main_logger.info('hello, I am running.')


    if (config.scheduler == 1):
        while True:
            now = time.ctime().split(' ')
            days = ['Mon', 'Wed', 'Fri']

            if now[0] in days and now[3].split(':')[0] == '09':
                main_logger.info('suduyuru is going to run, time: '+ str(now[3]))
                clientOps.update_clients(creds.filename) #works..
                suduyuru()
                time.sleep(60*60)

            else:
                main_logger.info('checked the time, suduyuru has not been run, time is: '+ str(now[3]))
                time.sleep(60*60)
    
    elif (config.scheduler == 0):
        main_logger.info(str(time.ctime()))
        clientOps.update_clients(creds.filename) #works..
        suduyuru()


if __name__ == "__main__":
    main()







