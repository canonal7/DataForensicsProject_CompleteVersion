import os
import time
import uuid
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urlparse, urljoin


# Variables
ua = UserAgent()
proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

resource_path = 'resources/Revolution' # REPLACE WITH YOUR HTML FOLDER PATH

path_dict = ['barbiturates','dissociatives','drugs-precursors','opioids','benzos','cannabis','ecstasy','other','paraphernelia','prescription','psychodelics','rcs','reagents','steroids','stimulants','tobacco','weight-loss']

def send_tor_request(url):
    """
    Function to set up a tor connection and send a request under tor network
    :param url: the url to download
    :return: response
    """
    header = {'User-Agent': ua.random}
    cookies = {'revolution_marketplace_session' : 'eyJpdiI6IkJPWnlORlFwZWpIRkRjVFhsZURlWmc9PSIsInZhbHVlIjoiVXd5TVdlSnF2ZG1IMGZUMmRIOEdTcVZRcTBsaU9DQXlvKzl5UlBGbUt0YzhVeGM4VmhRb3JDaVBiUno1WjJFTUNVbzBESEVyWHJraFhxSHhZZDF0UW9KUHo5cGR6RU9TUFZuQ2dlL3ZwN1RtZ1hZOWlKMzU0TGtxbXExY2JsdXciLCJtYWMiOiI2YmRmMjI1OTBiMzM1NTYzNDY0Yjk2Mjc2ZDgzNDI2NTA3YWVkNmVlZmY2NWY5NGFjZGJiOGUxN2M3NTdmNGIwIiwidGFnIjoiIn0%3D'}
    web_page = requests.get(url, headers=header, proxies=proxies, cookies=cookies)
    return web_page


def extract_internal_links(web_page):
    request_url = web_page.request.url
    domain = urlparse(request_url).netloc

    # Make soup
    soup = BeautifulSoup(web_page.content, "html.parser", from_encoding="iso-8859-1")

    urls = set()

    # Get all internal links
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        href = urljoin(request_url, href).strip("/")

        if href == "" or href is None:
            # href empty tag
            continue

        if urlparse(href).netloc != domain:
            # external link
            continue

        urls.add(href)

    return list(urls)


if __name__ == '__main__':
    # Step 1: seed initialization
    seed = "http://6revo64bqleix3vnixm7igazzdf5bx624bqaw6ipyjmhok72hmatzoad.onion/listings/category/drugs/"

    # web_page = send_tor_request(seed)
    # print(web_page.text)

    for category in path_dict:
        seed_new = seed + category
        try:
            web_page_new = send_tor_request(seed_new)
        except:
            print("Web Page download not succesful")
            continue
        filename = str(uuid.uuid4().hex) + ".html"
        path = os.path.join(resource_path, filename)
        with open(path, 'w', errors='ignore') as file:
            file.write(web_page_new.text)
            print(f"URL {seed_new} saved under the name {filename}")

    # # Step 2: creation of vivited list and queue (BFS)
    # visited = set()
    # queue = deque()

    # # Step 3: add the seed to the queue
    # queue.append(seed)

    # # Step 4: Iterate over the queue until it's empty
    # exit_condition_max_links = 20
    # while queue and len(visited) < exit_condition_max_links:
    #     url = queue.popleft()

    #     if url not in visited:
    #         # Send tor request to download the page
    #         web_page = send_tor_request(url)
    #         time.sleep(2)

    #         # Update the visited pages
    #         visited.add(url)

    #         # Save the page into the download folder
    #         filename = str(uuid.uuid4().hex) + ".html"
    #         path = os.path.join(resource_path, filename)
    #         with open(path, 'w') as file:
    #             file.write(web_page.text)
    #         print(f"URL {url} saved under the name {filename}")

    #         # Extract all the internal links
    #         new_urls = extract_internal_links(web_page)
    #         for new_url in new_urls:
    #             if new_url not in queue and new_url not in visited:
    #                 queue.append(new_url)