import dbOps
import scrapOps


def main():
    db = dbOps.connect_to_database('root', 'example')
    html_txt = 'login module will return the text of mysu html page'
    duyuru_dict = scrapOps.scraper(html_txt) #takes the html, scrapes announcements
        # and returns a neatly formatted list of dictionaries


if __name__ == "__main__":
    main()






