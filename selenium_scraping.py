import time
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

import scraping


def open_laptops_page():
    url = "https://rozetka.com.ua/ua/notebooks/c80004/"  # Rozetka laptops

    options = webdriver.ChromeOptions()
    # options.add_argument("headless")  # hide browser

    driver = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()),
                              options=options)

    driver.get(url)

    # driver.find_element(By.CSS_SELECTOR, ".pagination__list .pagination__item:last-of-type").click()

    time.sleep(3)

    print("Url is: " + driver.current_url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    pagination_list = soup.find(class_="pagination__list")
    pages = pagination_list.find_all(class_="pagination__item")
    first_page = pages[0].find("a").text.strip()
    last_page = pages[len(pages) - 1].find("a").text.strip()

    print(first_page, last_page)

    for page in range(int(first_page), int(last_page)):
        print("Scrapping page: {} ...".format(page))
        time.sleep(3)
        driver.execute_script('window.scrollTo({ top: 10000, behavior: "smooth" });')
        time.sleep(5)

        html = driver.page_source
        goods = scraping.get_laptops(html)
        goods_list_on_page = []

        for good in goods:
            goods_list_on_page.append(scraping.parse_good(good))

        with open(f"data/laptops_{str(page)}.json", "w") as file:
            json.dump(goods_list_on_page, file, indent=4, ensure_ascii=False)

        driver.find_element(By.CSS_SELECTOR, ".pagination__direction.pagination__direction--forward").click()
        time.sleep(3)
        driver.execute_script('window.scrollTo({ top: 0, behavior: "smooth" });')

    driver.close()
    driver.quit()


open_laptops_page()
