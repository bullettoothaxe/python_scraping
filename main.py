import scraping


def main():
    scraping.clone_resource_to_local_html()
    scraping.scrape_html_to_json()
    scraping.scrape_html_to_csv()


if __name__ == '__main__':
    main()
