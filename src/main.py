import dbOps
import scrapOps
import requests
import creds


def login_operation(username, password):
    # Login to mysu
    target_url = 'https://mysu.sabanciuniv.edu/announcements/en/all'
    login_url = 'https://login.sabanciuniv.edu/cas/login?service=https%3A%2F%2Fmysu.sabanciuniv.edu%2Fannouncements%2Fen%2Fall'
    evid = 'submit'
    login_data = {'username': username, 'password': password, 'execution': creds.exec, '_eventId': evid}

    with requests.Session() as s:
        r = s.post(login_url, data=login_data)
        r = s.get(target_url)
        return r.text


def main():
    db = dbOps.connect_to_database('root', 'example')
    html_txt = login_operation(creds.username, creds.password)
    duyuru_dict = scrapOps.scraper(html_txt) #takes the html, scrapes announcements
        # and returns a neatly formatted list of dictionaries
    #print title of first announcement
    print(duyuru_dict[0]['title'])


if __name__ == "__main__":
    main()






