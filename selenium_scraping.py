import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType


def open_laptops_page():
    url = "https://rozetka.com.ua/ua/notebooks/c80004/"  # Rozetka laptops

    options = webdriver.ChromeOptions()
    options.add_argument("headless")  # hide browser

    driver = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()),
                              options=options)

    driver.get(url)

    driver.find_element(By.CSS_SELECTOR, ".pagination__list .pagination__item:last-of-type").click()

    time.sleep(3)

    print("Url is: " + driver.current_url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    pagination_list_selector = "pagination__list"
    pagination_list = soup.find(class_=pagination_list_selector)
    pages = pagination_list.find_all(class_="pagination__item")
    first_page = pages[0].find("a").text.strip()
    last_page = pages[len(pages) - 1].find("a").text.strip()
    print(first_page, last_page)

    driver.close()
    driver.quit()


open_laptops_page()
