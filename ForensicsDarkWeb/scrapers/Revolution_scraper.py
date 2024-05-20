import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs
import os
import csv
import json
import time

csv_file_path = './csv/Revolution.csv'
json_file_path = './json/Revolution.json'

proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

res_dir = "./resources/Revolution"
ua = UserAgent()

products_array_csv = []
products_array_json = []

def is_correct_format_country(tag):
    for child in tag.children:
        if child.name and child.name!= "br":
            return False
    return True

def send_tor_request(url, cookie=None):
    header = {'User-Agent': ua.random}
    if cookie:
        header['Cookie'] = cookie
        
    web_page = requests.get(url, headers=header, proxies=proxies)
    return web_page

def scrape_page(url_path):
    iterator = 0
    dictionary = {}
    product_names_array = []
    product_prices_array = []
    product_country_array = []
    product_sellers_array = []
    for filename in os.listdir(url_path):
        # Creating unique products, prices and availability
        if filename.endswith(".html"):
            fullpath = os.path.join(url_path, filename)

            soup = BeautifulSoup(open(fullpath), "html.parser", from_encoding="iso-8859-1")
            
            product_names = soup.find_all("h3", attrs={"class":"font-bold mb-2 truncate text-gray-600 hover:text-gray-900 duration-300 hover:text-clip"})
            
            
            product_prices = soup.find_all("p", attrs={"class":"relative select-none text-lg font-semibold text-white"})
            
            product_country_divs = soup.find_all("div", attrs = {"class":"inline-block px-2 py-0.5 rounded text-xs font-medium bg-blue-50 hover:bg-blue-100 whitespace-nowrap text-blue-500 hover:text-blue-600 duration-300"})
            
            product_seller_divs = soup.find_all("div",attrs = {"class":"inline-flex group text-gray-400 hover:text-blue-600 duration-300 text-opacity-90 hover:text-opacity-100"})

            for product_name in product_names:
                product_names_array.append(product_name.text)
            for product_price in product_prices:
                price = product_price.text.strip()
                product_prices_array.append(price) 
                

            for product_country_div in product_country_divs:
                country_span= product_country_div.find_all("span")[1]
                country = country_span.text.strip()
                product_country_array.append(country)
            for product_seller_div in product_seller_divs:
                seller_anchor = product_seller_div.find("a")
                seller = seller_anchor.text
                
                product_sellers_array.append(seller)
                
    json_array_products = []
    csv_array_products = []
    for i in range (len(product_sellers_array)):
        product_object = {"product_name": product_names_array[i],
                          "product_seller":product_sellers_array[i],
                          "product_price":product_prices_array[i],
                          "product_country": product_country_array[i]
                          }
        json_array_products.append(product_object)

        product_array = [product_names_array[i],product_sellers_array[i],product_prices_array[i],product_country_array[i]]
        csv_array_products.append(product_array)
        
    with open(csv_file_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['Product', 'Seller', 'Price', "Country"]
        writer.writerow(header)
        for row in csv_array_products:
            writer.writerow(row)
    
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        
        json.dump(json_array_products, jsonfile, indent=4)
    
    
    #         products = soup.find_all('div', attrs={"class":"product-layout col-lg-3 col-md-3 col-sm-6 col-xs-12"})
    #         all_anchor_tags = soup.find_all('a')

            
            
    #         # print(products)
    #         # print("")
    #         # print(filename)
    #         # print("")
    #         for product in products:
    #             # print(product)
    #             try:
                    
    #                 product_name_center = product.find('center')
    #                 # print(product_name_center.find('a').text)
    #                 product_name = product_name_center.find("a").text.strip()

    #                 product_country_center = product.find_all('center')[2]

    #                 product_seller_center = product.find_all('a')[2]
    #                 product_seller = product_seller_center.text.strip()
    #                 print(product_seller)

    #                 product_price_center = product.find_all('center')[4]
    #                 product_price = product.find("b").text.strip()
    #                 print(product_price)

    #                 text = ""
    #                 if product_country_center and is_correct_format_country(product_country_center):

    #                     for content in product_country_center.contents:
    #                         # print(content.text)
    #                         if content.name == 'br':
    #                             break
    #                         else:
    #                             text += content if isinstance (content, str) else content.text
    #                 if len(text)>0:
    #                     text = text.split(':')[1]
    #                     product_country = text.strip()
    #                 else:
    #                     product_country = "N/A"
    #             except:
    #                 continue
                
    #             product_row = [product_name,product_seller,product_price,product_country]
    #             products_array_csv.append(product_row)
    #             print(product_row, '\n')

    #             product_object = {"product_name": product_name,
    #                                "product_seller": product_seller,
    #                                "product_price":product_price,
    #                                "product_country":product_country
    #                                }
    #             print(product_object,'\n')
    #             products_array_json.append(product_object)

    # with open(csv_file_path, 'w', encoding='utf-8', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     header = ['Product', 'Seller', 'Price', "Country"]
    #     writer.writerow(header)
    #     for row in products_array_csv:
    #         writer.writerow(row)
    
    # with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        
    #     json.dump(products_array_json, jsonfile, indent=4)



if __name__ == '__main__':
    # seed = "http://xv3dbyx4iv35g7z2uoz2yznroy56oe32t7eppw2l2xvuel7km2xemrad.onion/store/nojs/"
    # # seed = "http://xv3dbyx4iv35g7z2uoz2yznroy56oe32t7eppw2l2xvuel7km2xemrad.onion/store/nojs/index.php?route=product/product&product_id=2133"

    # download_and_scrape_example(seed)
    
    # url_path = "resources"
    # # scrape_example(url_path)
    scrape_page(res_dir)