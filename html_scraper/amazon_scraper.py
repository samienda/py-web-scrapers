from datetime import datetime
import requests
import csv
import bs4


def get_page_html(url):
    response = requests.get(url=url, headers=)
    return 0


def extract_product_info(url):
    product_info = {}
    print(f'Scraping URL: {url}')
    html = get_page_html(url)


if __name__ == "__main__":
    with open(r"C:/Users/SAMI/Documents/py-web-scrapers/html_scraper/amazon_products_urls.csv", encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        for row in reader:
            url = row[0]
            print(url)
