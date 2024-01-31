from bs4 import BeautifulSoup


def make_soup(html_text):
    """open html text and return a soup object"""
    soup = BeautifulSoup(html_text, 'lxml')
    return soup    

def get_announcements(soup):
    """The function will get a soup object of the 
    announcements page and return a list
    containing the announcements"""
    all_announcements = []
        
    even_ann = soup.find_all('tr', class_='even')
    odd_ann = soup.find_all('tr', class_='odd') # this handles the weird
        # first and last announcement classes
    for x in range(12):
        all_announcements.append(odd_ann[x])
        all_announcements.append(even_ann[x])
    all_announcements.append(odd_ann[12]) # this handles the last announcement
        #the announcements are ordered from newest to oldest
    return all_announcements
    
def parse_announcement(ann):
    """The function will get a soup object of an announcement
    and return a dictionary containing the announcement"""
    try:
        announcement = {}
        announcement['title'] = ann.find('td', class_='views-field views-field-title list list-new').text.strip()
        announcement['views'] = ann.find('td', class_='views-field views-field-totalcount list-new').text.strip()
        extension = ann.find('td', class_='views-field views-field-title list list-new').a['href']
        announcement['link'] = 'https://mysu.sabanciuniv.edu' + extension
        announcement['new']=True
        return announcement
    except AttributeError:
        announcement = {}
        announcement['title'] = ann.find('td', class_='views-field views-field-title list list-old').text.strip()
        announcement['views'] = ann.find('td', class_='views-field views-field-totalcount list-old').text.strip()
        extension = ann.find('td', class_='views-field views-field-title list list-old').a['href']
        announcement['link'] = 'https://mysu.sabanciuniv.edu' + extension
        announcement['new']=False
        return announcement



def scraper(html_text):
    """The function will get an html file of the 
    announcements page and return a list of
    dictionaries containing the announcements"""
    soup = make_soup(html_text)
    announcements = get_announcements(soup)
    Duyurular = []
    for ann in announcements:
        Duyuru = parse_announcement(ann)
        Duyurular.append(Duyuru)
    return Duyurular