import pymongo
from time import sleep


#logging setup
import logging

logger = logging.getLogger(__name__)


def get_database(user, passw, host='host.docker.internal', port=27017):
    # Get a database instance
    client = pymongo.MongoClient(host, port, username=user, password=passw)

    # There was an issue with the host where localhost was referring to the container itself, 
    # this solution (host='host.docker.internal') now refers to the host machine which is working now.
    # However, if it breaks, try setting static ips in the docker-compose file

    db_data = client.Duyurular #hard-coded database name because the variable didn't work
    return db_data

def test_connection(database):
    # Test the connection
    try:
        characters = []
        for character in database.test.find():
            characters.append(character)
    except:
        return False
    return True

def connect_to_database(user, passw, host='SUDuyuru-mongo', port=27017):
    # Connect to the database
    logger.debug("Connecting to database...")
    db = get_database(user, passw, host, port)

    #only return db once connection to db is successful
    attempts = 0
    while (not test_connection(db)) and (attempts < 5):
        attempts += 1
        logger.warning("Connection failed, retrying...")
        if (attempts == 5):
            logger.error("Connection failed after 5 attempts")
            return None
        sleep(10)

    logger.info("Connection to database is successful")
    return db

#group of functions to handle the announcements

def insert_announcements(announcements, database):
    """The function will insert the announcements into the database"""
    
    logger.debug("Inserting announcements into the database...")
    
    for announcement in announcements:
        if not exists(announcement, database):
            database.announcements.insert_one(announcement)
            #set age to 0, this will handle old announcements
            database.announcements.update_one({'link': announcement['link']},
                                              {"$set": {'age' : 0}},
                                                upsert = True)
        else:
            #this handles new announcements becoming old
            database.announcements.update_one({'link': announcement['link']}, 
                                              {"$set": {'new' : announcement['new']}},
                                                upsert = True)
            logger.debug("A 'new' flag was updated")
    
    logger.info("Insertion of new announcements complete")

def exists(announcement, database):
    """The function will check if the announcement exists in the database"""
    test = database.announcements.find_one({'link': announcement['link']})
    if test == None:
        return False
    else:
        return True
    
def wipe_announcements(database):
    """The function will wipe all the announcements from the database"""
    logger.warning("Wiping all announcements...")
    database.announcements.delete_many({})
    logger.info("Wipe complete")

def get_all_announcements(database):
    """The function will return all the announcements in the database"""
    logger.debug("Getting all announcements from the database...")
    announcements = []
    for announcement in database.announcements.find():
        announcements.append(announcement)
    logger.debug("Retrieval complete")
    return announcements

def get_sent_announcements(database):
    """The function will return all the announcements in the database"""
    logger.debug("Getting all sent announcements from the database...")
    announcements = []
    for announcement in database.announcements.find({'sent': True}):
        announcements.append(announcement)
    logger.debug("Retrieval complete")
    return announcements

def get_unsent_announcements(database):
    """The function will return all the announcements in the database"""
    logger.debug("Getting all unsent announcements from the database...")
    announcements = []
    for announcement in database.announcements.find({'sent': {'$not': {'$eq': True}} }):
        announcements.append(announcement)
    logger.info("Retrieved "+ str(len(announcements)) +" unsent announcements from the database")
    return announcements

def mark_as_sent(announcement, database):
    """The function will mark the announcement as sent"""
    database.announcements.update_one({'link': announcement['link']}, 
                                      {"$set": {'sent' : True}},
                                        upsert = True)
    logger.debug(f"{announcement['title']} marked as sent")

def increment_ann_age(database):
    """The function will increment the age of all announcements"""
    logger.debug("Incrementing the age of all announcements...")
    database.announcements.update_many({}, {"$inc": {'age' : 1}})
    logger.debug("Increment complete")

def wipe_old_announcements(database):
    """The function will wipe all the old announcements from the database"""
    logger.warning("Wiping the old announcements (age greater than 15)...")
    database.announcements.delete_many({'age': {'$gt': 15}})
    logger.info("Wipe complete")

#group of functions to handle clients

def exists_client(client, database):
    """The function will check if the client exists in the database"""
    test = database.clients.find_one({'email': client})
    if test == None:
        return False
    else:
        return True

def insert_client(client, database):
    """The function will get the email, make a dictionary and insert it into the database"""
    formatted_client = {'email': client}
    if not exists_client(client, database):
        if valid_client(client):
            database.clients.insert_one(formatted_client)
            logger.debug(f"{client} inserted into the database")
        else:
            logger.warning(f"{client} is not a valid email")
    else:
        logger.debug(f"{client} already exists in the database")  

def wipe_client(client, database):
    """The function will wipe the client from the database"""
    if exists_client(client, database):
        database.clients.delete_one({'email': client})
        logger.warning(f"{client} wiped from the database")
    else:
        logger.warning(f"{client} does not exist in the database, cannot wipe")

def valid_client(client):
    """The function will check if the client has a sabanci email"""
    if client.endswith('@sabanciuniv.edu'):
        return True
    else:
        return False
    
def get_all_clients(database):
    """The function will return all the clients in the database"""
    logger.debug("Getting all clients from the database...")
    clients = []
    for client in database.clients.find():
        clients.append(client)
    logger.info("Retrieved "+ str(len(clients)) +" clients from the database")
    return clients