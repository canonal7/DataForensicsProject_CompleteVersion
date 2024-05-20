import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs
import os
import csv
import json

csv_file_path = '../csv/DeDope.csv'
json_file_path = '../json/DeDope.json'

proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

res_dir = "../resources/DeDope"
ua = UserAgent()


def send_tor_request(url, cookie=None):
    header = {'User-Agent': ua.random}
    if cookie:
        header['Cookie'] = cookie

    web_page = requests.get(url, headers=header, proxies=proxies)
    return web_page


def download_and_scrape_example(seed, cookie=None):
    # Crawl the page
    web_page = send_tor_request(seed, cookie)

    # Use the web page content to scrape the web page
    soup = BeautifulSoup(web_page.content, "html.parser", from_encoding="iso-8859-1")

    # Scraping
    # soup.find("Scraping rule HERE")
    DeDope_list = []
    for tr in soup.findAll('table')[0].tbody.findAll('td'):
        print(tr.text.strip())
        DeDope_list.append(tr.text.strip())

    # Creating unique products, prices and availability
    DeDope_dictionary = {}
    iterator = 0

    #Since we have 3 categories (Product, Price, Availability), we can divide them by 3

    for item in DeDope_list:
        if iterator % 3 == 0:
           i = iterator // 3
           product = 'Product' + str(i)
           DeDope_dictionary[product] = item
           iterator += 1
        elif iterator % 3 == 1:
            i = iterator // 3
            price = 'Price' + str(i)
            DeDope_dictionary[price] = item
            iterator += 1
        elif iterator % 3 == 2:
            i = iterator // 3
            availability = 'Quantity' + str(i)
            DeDope_dictionary[availability] = item
            iterator += 1
    print(DeDope_dictionary)





def scrape_example(url_path):
    # Use the web page content to scrape the web page

    iterator = 0
    DeDope_dictionary = {}
    for filename in os.listdir(url_path):
        # Creating unique products, prices and availability
        if filename.endswith(".html"):
            fullpath = os.path.join(url_path, filename)

            soup = BeautifulSoup(open(fullpath), "html.parser", from_encoding="iso-8859-1")

            # Scraping
            DeDope_list = []
            # Find all tables in the HTML
            tables = soup.findAll('table')

            # Check if any tables are found
            if tables:
                for tr in soup.findAll('table')[0].tbody.findAll('td'):
                    print(tr.text.strip())
                    DeDope_list.append(tr.text.strip())

            else:
                print("No tables found in the HTML.")


            # Since we have 3 categories (Product, Price, Availability), we can divide them by 3

            for item in DeDope_list:
                if iterator % 3 == 0:
                    i = iterator // 3
                    key = 'Product' + str(i)
                elif iterator % 3 == 1:
                    i = iterator // 3
                    key = 'Price' + str(i)
                elif iterator % 3 == 2:
                    i = iterator // 3
                    key = 'Availability' + str(i)



                DeDope_dictionary[key] = item
                iterator += 1

    print(DeDope_dictionary)
    # Extract keys and values
    keys = [key for key in DeDope_dictionary.keys()]
    values = [DeDope_dictionary[key] for key in keys]

    # Write data to CSV
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(keys)
        writer.writerow(values)


    print("CSV file has been created successfully.")

    # Write data to JSON
    with open(json_file_path, 'w') as jsonfile:
        json.dump(DeDope_dictionary, jsonfile, indent=4)

    print("JSON file has been created successfully.")

if __name__ == '__main__':
    #seed = "http://4p6i33oqj6wgvzgzczyqlueav3tz456rdu632xzyxbnhq4gpsriirtqd.onion/index.php?cat=300"

    #download_and_scrape_example(seed)

    url_path = "../resources/DeDope"
    scrape_example(url_path)