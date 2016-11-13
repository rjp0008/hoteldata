#needs refactoring

import requests, bs4, sys
import selenium
from selenium.webdriver.support.ui import Select
from hotel import Hotel
import time

marriottRewardList = 'http://www.marriott.com/rewards/pointsGridPopUp.mi?awardType=Standard'

class MarriottHotel(Hotel):
    def __init__(self):
        Hotel.__init__(self)

prof = selenium.webdriver.FirefoxProfile(r'C:\Users\rjp00\AppData\Roaming\Mozilla\Firefox\Profiles\3y96a6tk.user')
hotels = []

browser = selenium.webdriver.Firefox(prof)

for x in range(0,15):
    hotels.clear()
    browser.get(marriottRewardList)
    select = Select(browser.find_element_by_id('category-tier'))
    select.select_by_index((x))
    browser.find_element_by_name("submit").click()
    time.sleep(5)
    soup = bs4.BeautifulSoup(browser.page_source)
    links = soup.select('a')
    for link in links:
        try:
            url = link.attrs['href']
            if '/hotels/rewards-points' in url:
                res = requests.get('http://www.marriott.com' + url)
                res.raise_for_status()
                newUrlPage = bs4.BeautifulSoup(res.text)
                newHotel = MarriottHotel()
                newHotel.name = newUrlPage.select('span[itemprop=name]')[0].text
                newHotel.address = newUrlPage.select('span[itemprop=streetAddress]')[0].text + " " + newUrlPage.select('span[itemprop=addressLocality]')[0].text
                newHotel.url=url
                newHotel.update_from_google()
                hotels.append(newHotel)
        except Exception as e:
            print(e)
            pass
    with open( '.\\data\\marriott\\'+str(x)+'.txt', 'w') as f:
        for hotel in hotels:
            f.write(hotel.name + "\n")
            f.write("\t" + hotel.url + "\n")
            try:
                f.write("\t" + str(hotel.address).encode(sys.stdout.encoding, errors='replace').decode('utf-8') + "\n")
            except:
                pass
            try:
                f.write("\t" + str(hotel.lat) + " " + str(hotel.lng) + "\n")
            except:
                pass