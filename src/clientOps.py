import pandas
import dbOps

#this is supposed to handle opening the excel of the clients, schedule client list update operations and handle them.


def open_csv(filename):
    try:
        df = pandas.read_csv(filename)
        print('CSV file opened successfully')
        return df
    except Exception as e:
        print('Error: ', e)
        return None


def who_sign_up(csv):
    """This function will return a dataframe containing the clients who signed up for the service."""
    #it should handle if the client has 2 entries, it should get the latest one using the timestamp

    #get the latest entry of each client
    latest_entries = csv.drop_duplicates(subset=['What is your @sabanciuniv.edu email?'], keep='last')
    
    #get the clients who signed up
    signed_up = latest_entries[latest_entries['What action would you like to perform?'] == 'Sign up']

    return signed_up


def who_opt_out(csv):
    """This function will return a dataframe containing the clients who opted out of the service."""
    #it should handle if the client has 2 entries, it should get the latest one using the timestamp

    #get the latest entry of each client
    latest_entries = csv.drop_duplicates(subset=['What is your @sabanciuniv.edu email?'], keep='last')
    
    #get the clients who opted out
    opted_out = latest_entries[latest_entries['What action would you like to perform?'] == 'Opt out']

    return opted_out


def update_sign_up(db, sign_up_list):
    """This function will insert the emails of clients who signed up into the database."""
    for email in sign_up_list['What is your @sabanciuniv.edu email?']:
        dbOps.insert_client(email, db)


def update_opt_out(db, opt_out_list):
    """This function will wipe the emails of clients who opted out from the database."""
    for email in opt_out_list['What is your @sabanciuniv.edu email?']:
        dbOps.wipe_client(email, db)


def update_clients(filename):
    """This function will be called by the scheduler to handle the client list update operations."""

    #open the csv file
    csv = open_csv(filename)

    #connect to the database
    db = dbOps.connect_to_database('root', 'example')

    #who does what
    signed_up = who_sign_up(csv)
    opted_out = who_opt_out(csv)

    #update the clients
    print('Updating the clients list...')
    update_sign_up(db, signed_up)
    update_opt_out(db, opted_out)
    print('Update complete')
