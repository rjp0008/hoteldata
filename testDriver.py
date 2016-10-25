from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

hyatt_category_page = 'https://www.hyatt.com/gp/en/awards/hyatt_category_display.jsp?_DARGS=/gp/en/awards/hyatt_category_display.jsp'
browser = webdriver.Firefox()
browser.get(hyatt_category_page)
select = Select(browser.find_element_by_tag_name('select'))
select.select_by_value('2')

time.sleep(2)
links = browser.find_elements_by_tag_name('a')
hotel_links = []
for link in links:
    url = link.get_attribute('href')
    if(str(url).__contains__('/hotel/')):
        hotel_links.append(url)
        print(url)
addresses = []
for link in hotel_links:
    browser.get(link)
    elements = browser.find_elements_by_class_name('address')
    address = ""
    for item in elements:
        address = address + item.text + " "
    addresses.append(address)
    print(address)
