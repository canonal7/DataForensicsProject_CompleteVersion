import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs
import os
import csv
import json

list = ['Smokeables','BitPharma','CanUK','DeDope','pds','EuCanna','BrainMagic','NLGrowers']
list_of_lists= []
for element in list:
    path_string = './resources/' + element
    csv_string = './csv/' + element + '.csv'
    json_string = './json/' + element + '.json'
    list_of_lists.append([path_string, csv_string, json_string])

#csv_file_path = ['../csv/Test.csv']

#json_file_path = ['../json/Test.json']

#res_dir = ["../resources/Test"]

proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}


ua = UserAgent()


def send_tor_request(url, cookie=None):
    header = {'User-Agent': ua.random}
    if cookie:
        header['Cookie'] = cookie

    web_page = requests.get(url, headers=header, proxies=proxies)
    return web_page



def scrape_example(path):
    # Use the web page content to scrape the web page

    iterator = 0
    tbody_dictionary = {}

    for filename in os.listdir(path[0]):
        # Creating unique products, prices and availability
        if filename.endswith(".html"):
            fullpath = os.path.join(path[0], filename)

            soup = BeautifulSoup(open(fullpath, errors="ignore"), "html.parser", from_encoding="utf-8" )
            # soup = BeautifulSoup(open(fullpath), "html.parser", from_encoding="utf-8")

            # Scraping
            tbody_list = []
            # Find all tables in the HTML
            tables = soup.findAll('table')

            # Check if any tables are found
            if tables:
                for tr in soup.findAll('table')[0].tbody.findAll('td'):
                    print(tr.text.strip())
                    tbody_list.append(tr.text.strip())

            else:
                print("No tables found in the HTML.")


            # Since we have 3 categories (Product, Price, Availability), we can divide them by 3
            
            for item in tbody_list:
                if iterator % 3 == 0:
                    i = iterator // 3
                    key = 'Product' + str(i)

                elif iterator % 3 == 1:
                    i = iterator // 3
                    key = 'Price' + str(i)
                elif iterator % 3 == 2:
                    i = iterator // 3
                    key = 'Availability' + str(i)



                tbody_dictionary[key] = item
                iterator += 1

    # print(tbody_dictionary)
    # Extract keys and values
    keys = [key for key in tbody_dictionary.keys()]
    values = [tbody_dictionary[key] for key in keys]

    # Write data to CSV
    with open(path[1], 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['Product', 'Price', 'Availability']
        writer.writerow(header)
        for i in range (0,len(keys)-3,3):
            writer.writerow(values[i:i+3])
        # writer.writerow(values)


    print("CSV file has been created successfully.")


    products = []

    for i in range(0, len(tbody_list)-3, 3):
        product ={"Product": tbody_list[i], "Price": tbody_list[i+1], "Availability": tbody_list[i+2]}
        products.append(product)
    # Write data to JSON
    with open(path[2], 'w', encoding='utf-8') as jsonfile:
        
        json.dump(products, jsonfile, indent=4)

    print("JSON file has been created successfully.")

if __name__ == '__main__':
    for path in list_of_lists:
        scrape_example(path)