from datetime import datetime
import time
import requests
import csv
import bs4
from fake_useragent import UserAgent


random_user_agent = UserAgent().random
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
REQUEST_HEADER = {
    'User-Agent': random_user_agent,
    'Accept-Language': 'en-US, en;q=0.5',
}


def get_page_html(url):
    time.sleep(5)
    response = requests.get(url=url, headers=REQUEST_HEADER, timeout=20)
    return response.content


def get_product_price(soup):
    main_price_span = soup.find('span', attrs={
        "class": "a-price a-text-price a-size-medium apexPriceToPay"
    })
    # print(main_price_span)
    price_span = main_price_span.findAll('span')
    for span in price_span:
        price = span.text.strip().replace('$', '').replace(',', '')
        try:
            return float(price)
        except ValueError:
            print("price value can not be parsed")
            exit()


def get_product_title(soup):
    product_title = soup.find('span', id='productTitle')

    return product_title.text.strip()


def get_product_rating(soup):
    prodcut_ratings = soup.find(
        'div', attrs={
            'id': "averageCustomerReviews",
        })

    prodcut_rating_section = prodcut_ratings.find('i', attrs={
        "class": "a-icon-star"
    })

    prodcut_rating_span = prodcut_rating_section.find('span', attrs={
        "class": "a-icon-alt"
    })

    try:
        rating = prodcut_rating_span.text.strip().split()

        return float(rating[0])
    except ValueError:
        print("product rating can not be parsed")
        exit()


def get_product_technical_details(soup):
    details = {}
    technical_details_section = soup.find('div', id="prodDetails")
    data_table = technical_details_section.findAll(
        'table', class_="prodDetTable")

    for table in data_table:
        table_rows = table.findAll('tr')

        for row in table_rows:
            row_key = row.find('th').text.strip()
            row_value = row.find('td').text.strip().replace('\n', '')

            details[row_key] = row_value

    return details



def extract_product_info(url):
    product_info = {}
    # print(f'Scraping URL: {url}')
    html = get_page_html(url=url)
    # print(html)
    soup = bs4.BeautifulSoup(html, 'lxml')
    product_info['price'] = get_product_price(soup=soup)
    product_info['title'] = get_product_title(soup=soup)
    product_info['rating'] = get_product_rating(soup=soup)

    product_info.update(get_product_technical_details(soup=soup))

    return product_info


if __name__ == "__main__":
    products_data = []
    with open(r"C:/Users/SAMI/Documents/py-web-scrapers/html_scraper/amazon_products_urls.csv", encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        for row in reader:
            # print(row)
            url = row[0]
            products_data.append(extract_product_info(url=url))

    output_file_name = 'output-{}.csv'.format(
        datetime.today().strftime("%m-%d-%y"))

    with open(output_file_name, 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(products_data[0].keys())

        for product in products_data:
            writer.writerow(product.values())
