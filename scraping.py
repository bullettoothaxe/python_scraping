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


def scrape_saved_html(html):
    goods_selector = "goods-tile"
    src = read_from_local_html(html)
    soup = BeautifulSoup(src, "lxml")
    all_laptops = soup.find_all(class_=goods_selector)
    return all_laptops


def parse_good(good):
    title_selector = "goods-tile__heading"
    price_selector = "goods-tile__price"
    img_selector = "goods-tile__picture"

    id_ = good.find(class_="goods-tile__inner").get("data-goods-id").strip()
    title = good.find(class_=title_selector).text.strip()
    price = good.find(class_=price_selector).find(class_="goods-tile__price-value").text.strip().replace(" ", "")
    img_path = good.find(class_=img_selector).find("img").get("src").strip()

    return {
        "id": id_,
        "title": title,
        "price": price,
        "img_path": img_path,
        "currency": "UAH"
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
                "Currency"
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
                )
            )


def scrape_html_to_csv(html=local_html_file):
    goods = scrape_saved_html(html)
    save_goods_into_csv(goods)

