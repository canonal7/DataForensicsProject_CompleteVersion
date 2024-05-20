import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs
import os
import csv
import json

csv_file_path = '../csv/MidlandCity.csv'
json_file_path = '../json/MidlandCity.json'

proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

res_dir = "../resources/MidlandCity"
ua = UserAgent()


def send_tor_request(url, cookie=None):
    header = {'User-Agent': ua.random}
    if cookie:
        header['Cookie'] = cookie

    web_page = requests.get(url, headers=header, proxies=proxies)
    return web_page


def scrape_example(url_path):
    # Use the web page content to scrape the web page

    iterator = 0
    dictionary = {}
    for filename in os.listdir(url_path):
        # Creating unique products, prices and availability
        if filename.endswith(".html"):
            fullpath = os.path.join(url_path, filename)

            soup = BeautifulSoup(open(fullpath), "html.parser", from_encoding="iso-8859-1")

            looper = soup.find_all('div' ,{'class':['item', 'item2']})

            list = []

            for element in looper:
                if element.text.strip() != 'PayPal Transfer' and element.text.strip() != 'PayPal Account' and element.text.strip() != '$75' and element.text.strip() != '$120':
                    list.append(element.text.strip())
                    #print(element.text.strip())

            for item in list:
                if iterator % 2 == 0:
                    i = iterator // 2
                    key = 'Product' + str(i)
                elif iterator % 2 == 1:
                    i = iterator // 2
                    key = 'Price' + str(i)

                dictionary[key] = item
                iterator += 1

            # Extract keys and values
            keys = [key for key in dictionary.keys()]
            values = [dictionary[key] for key in keys]

    print(dictionary)
    # Write data to CSV
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(keys)
        writer.writerow(values)

    print("CSV file has been created successfully.")

    # Write data to JSON
    with open(json_file_path, 'w') as jsonfile:
        json.dump(dictionary, jsonfile, indent=4)

    print("JSON file has been created successfully.")

if __name__ == '__main__':

    url_path = "../resources/MidlandCity"
    scrape_example(url_path)