import selenium
from selenium.webdriver.support.ui import Select
import time
import sys
from hotel import Hotel

class HyattHotel(Hotel):
    def __init__(self):
        Hotel.__init__(self)


def get_hotel_urls(browser):
    links = browser.find_elements_by_tag_name('a')
    hotel_links = []
    for link in links:
        url = link.get_attribute('href')
        if (str(url).__contains__('/hotel/')):
            hotel_links.append(url)
    return hotel_links

def hotel_factory(browser,urls):
    hotels = []
    for url in urls:
        newHotel = HyattHotel()
        newHotel.url = url
        try:
            browser.get(newHotel.url)
        except selenium.common.exceptions.WebDriverException:
            break

        elements = browser.find_elements_by_class_name('address')
        address = ""
        for item in elements:
            address = address + item.text + " "
        newHotel.address = address

        elements = browser.find_elements_by_class_name('homePropertyName')
        name = ""
        for item in elements:
            name = name + item.text + " "
        newHotel.name = name
        hotels.append(newHotel)
    return hotels

hyatt_category_page = 'https://www.hyatt.com/gp/en/awards/hyatt_category_display.jsp?_DARGS=/gp/en/awards/hyatt_category_display.jsp'
prof = selenium.webdriver.FirefoxProfile(r'C:\Users\rjp00\AppData\Roaming\Mozilla\Firefox\Profiles\3y96a6tk.user')


browser = selenium.webdriver.Firefox(prof)
browser.get(hyatt_category_page)
select = Select(browser.find_element_by_tag_name('select'))
category_levels = (len(select.options))

for x in range(3,category_levels+1):
    browser.get(hyatt_category_page)
    select = Select(browser.find_element_by_tag_name('select'))
    select.select_by_value(str(x))
    time.sleep(2)
    hotel_urls = get_hotel_urls(browser)
    hotels = hotel_factory(browser,hotel_urls)
    with open(str(x) + 'hyatt.txt', 'w') as f:
        for hotel in hotels:
            f.write(hotel.name + "\n")
            f.write("\t" + hotel.url + "\n")
            try:
                f.write("\t" + str(hotel.address).encode(sys.stdout.encoding,errors='replace').decode('utf-8') + "\n")
            except:
                pass
browser.quit()