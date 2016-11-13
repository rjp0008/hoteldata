#needs refactoring

import requests, bs4, sys
from hotel import Hotel
countryList = 'https://www.ihg.com/destinations/us/en/explore'

class IHGHotel(Hotel):
    def __init__(self):
        Hotel.__init__(self)

hotels = []

def getHotelInfo(link):
    hotel = IHGHotel()
    hotel.url = link
    res = requests.get(link)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
    address = soup.select('span[itemprop="address"]')
    if len(address) is 0:
        address = soup.select('div[itemprop="address"]')
    if len(address) is 0:
        address = soup.select('p[itemprop="address"]')
    try:
        hotel.address = address[0].getText().replace('\n','')
    except:
        pass
    hotel.name = soup.select('title')[0].getText()
    hotel.update_from_google()
    hotels.append(hotel)
    with open('.\\data\\ihg\\ihg.txt', 'a') as f:
        try:
            f.write(str(hotel.name).encode(sys.stdout.encoding, errors='replace').decode('utf-8').strip() + "\n")
        except:
            pass
        try:
            f.write("\t" + hotel.url + "\n")
        except:
            pass
        try:
            f.write("\t" + str(hotel.address).encode(sys.stdout.encoding,errors='replace').decode('utf-8').strip() + "\n")
        except:
            pass
        try:
            f.write("\t" + str(hotel.lat) + " " + str(hotel.lng) + "\n")
        except:
            pass

def possibleValidLink(url):
    if 'airport-hotels' in url:
        return False
    if 'waterpark-holidome-hotels' in url:
        return False
    if 'beach-hotels' in url:
        return False
    if 'pet-friendly-hotels' in url:
        return False
    return True

def drillDown(link: str, ignoreList: list):
    print(link)
    try:
        res = requests.get(link)
    except:
        return
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        return
    soup = bs4.BeautifulSoup(res.text)
    links = soup.select('a')
    for item in links:
        try:
            newLink = item.attrs['href']
        except KeyError:
            if newLink not in ignoreList:
                ignoreList.append(newLink)
            continue
        if 'http' not in newLink:
            if newLink not in ignoreList:
                ignoreList.append(newLink)
            continue
        if 'explore' in newLink:
            continue
        if not possibleValidLink(newLink):
            break
        if '/destinations/us/en/' in newLink and newLink not in ignoreList:
            ignoreList.append(newLink)
            drillDown(newLink,ignoreList)
        if 'hotel-reviews' in newLink:
            if newLink not in ignoreList:
                ignoreList.append(newLink)
            continue
        if '/hoteldetail' in newLink and newLink not in ignoreList:
            ignoreList.append(newLink)
            getHotelInfo(newLink)

ignoreLinks = []
res = requests.get(countryList)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text)
links = soup.select('li > a')
for item in links:
    link = item.attrs['href']
    if '/destinations/us/en/' in link:
        ignoreLinks.append(link)
        drillDown(link,ignoreLinks)