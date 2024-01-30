import pymongo
import pprint


def get_database(user, passw, host='host.docker.internal', port=27017):
    # Get a database instance
    client = pymongo.MongoClient(host, port, username=user, password=passw)

    # There was an issue with the host where localhost was referring to the container itself, 
    # this solution (host='host.docker.internal') now refers to the host machine which is working now.
    # However, if it breaks, try setting static ips in the docker-compose file

    db_data = client.Duyurular #hard coded database name because the variable didn't work
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

def connect_to_database(user, passw, host='host.docker.internal', port=27017):
    # Connect to the database
    print("Connecting to database...")
    db = get_database(user, passw, host, port)
    if test_connection(db):
        print("Connection successful")
    else:
        print("Connection failed")
    return db

