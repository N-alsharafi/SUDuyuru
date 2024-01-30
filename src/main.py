from bs4 import BeautifulSoup
import dbOps


def main():
    db = dbOps.connect_to_database('root', 'example')


if __name__ == "__main__":
    main()






