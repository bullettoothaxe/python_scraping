import time

from bs4 import BeautifulSoup
import requests
import json
import csv

url = "https://rozetka.com.ua/ua/notebooks/c80004/"  # Rozetka laptops

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) "
                  "Version/11.0 Mobile/15A5341f Safari/604.1 "
}

local_html_file = "_index.html"
local_json_file = "goods.json"
local_csv_file = "goods.csv"

goods_selector = "goods-tile"

SLEEP_BETWEEN_PAGES_SEC = 3


def save_into_local_html(src):
    with open(local_html_file, "w") as file:
        file.write(src)


def read_from_local_html(file):
    with open(file) as file_:
        return file_.read()


def clone_resource_to_local_html():
    src = requests.get(url, headers=headers).text
    save_into_local_html(src)


def save_goods_into_json(goods_list, json_file=local_json_file):
    with open(json_file, "w") as file:
        json.dump(goods_list, file, indent=4, ensure_ascii=False)


def get_laptops(src):
    soup = BeautifulSoup(src, "lxml")
    all_laptops = soup.find_all(class_=goods_selector)
    return all_laptops


def scrape_saved_html(html):
    src = read_from_local_html(html)
    return get_laptops(src)


def parse_good(good):
    title_selector = "goods-tile__heading"
    price_selector = "goods-tile__price"
    img_selector = "goods-tile__picture"
    disabled_item_selector = "goods-tile_state_disabled"

    id_ = good.find(class_="goods-tile__inner").get("data-goods-id").strip()
    title = good.find(class_=title_selector).text.strip()
    price = good.find(class_=price_selector).find(class_="goods-tile__price-value").text.strip().replace(" ", "")
    img_path = good.find(class_=img_selector).find("img").get("src").strip()
    disabled = disabled_item_selector in good.get("class")

    return {
        "id": id_,
        "title": title,
        "price": price,
        "img_path": img_path,
        "currency": "UAH",
        "active": not disabled
    }


def scrape_html_to_json(html=local_html_file):
    goods = scrape_saved_html(html)
    goods_list = []

    for good in goods:
        goods_list.append(parse_good(good))

    save_goods_into_json(goods_list)


def save_goods_into_csv(goods, csv_file_path=local_csv_file):
    with open(csv_file_path, "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "ID",
                "Title",
                "Price",
                "Image",
                "Currency",
                "Active"
            )
        )

    for good in goods:
        with open(csv_file_path, "a", encoding="utf-8") as file:
            good_parsed = parse_good(good)
            writer = csv.writer(file)
            writer.writerow(
                (
                    good_parsed['id'],
                    good_parsed['title'],
                    good_parsed['price'],
                    good_parsed['img_path'],
                    good_parsed['currency'],
                    good_parsed['active'],
                )
            )


def scrape_html_to_csv(html=local_html_file):
    goods = scrape_saved_html(html)
    save_goods_into_csv(goods)


##### Paginated #####

def find_pagination_start_and_finish_values(html=local_html_file):
    pagination_list_selector = "pagination__list"
    src = read_from_local_html(html)
    soup = BeautifulSoup(src, "lxml")
    pagination_list = soup.find(class_=pagination_list_selector)
    pages = pagination_list.find_all(class_="pagination__item")
    first_page = pages[0].find("a").text.strip()
    last_page = pages[len(pages) - 1].find("a").text.strip()
    return [first_page, last_page]


def page_url_postfix(page):
    return f"page={page}/"


def scrape_for_all_pages():
    print("Run scrapping with pagination!")
    [first_page, last_page] = find_pagination_start_and_finish_values()
    # for page in range(int(first_page), int(last_page) + 1):
    for page in range(1, 3):
        print(f"Scrape on Page: {page}...")
        src = requests.get(url + page_url_postfix(page), headers=headers).text

        time.sleep(SLEEP_BETWEEN_PAGES_SEC)

        goods = get_laptops(src)
        goods_list_on_page = []

        for good in goods:
            goods_list_on_page.append(parse_good(good))

        with open(f"data/laptops_{str(page)}.json", "w") as file:
            json.dump(goods_list_on_page, file, indent=4, ensure_ascii=False)

    print("Finish!")

