import requests, bs4, sys
countryList = 'https://www.ihg.com/destinations/us/en/explore'

class HyattHotel:
    def __init__(self):
        self.url = ""
        self.address = ""
        self.name = ""

    def __str__(self):
        return self.url + " " + self.address

hotels = []

def getHotelInfo(link):
    hotel = HyattHotel()
    hotel.url = link
    res = requests.get(link)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
    address = soup.select('span[itemprop="address"]')
    hotel.address = address[0].getText()
    hotel.name = soup.select('h2[class="hi-hd-quick-info-address-heading"]')[0].getText()
    hotels.append(hotel)
    with open('ihg.txt', 'w') as f:
        for hotel in hotels:
            f.write(hotel.name + "\n")
            f.write("\t" + hotel.url + "\n")
            try:
                f.write("\t" + str(hotel.address).encode(sys.stdout.encoding,errors='replace').decode('utf-8') + "\n")
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

def drillDown(link,ignoreList):
    res = requests.get(link)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
    links = soup.select('a')
    for item in links:
        newLink = item.attrs['href']
        if 'explore' in newLink:
            continue
        if not possibleValidLink(newLink):
            break
        if '/destinations/us/en/' in newLink and newLink not in ignoreList:
            ignoreList.append(newLink)
            drillDown(newLink,ignoreList)
        if '/hoteldetail' in newLink:
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