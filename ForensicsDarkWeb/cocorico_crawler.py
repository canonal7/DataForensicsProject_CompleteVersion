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

resource_path = 'resources/Cocorico' # REPLACE WITH YOUR HTML FOLDER PATH


def send_tor_request(url):
    """
    Function to set up a tor connection and send a request under tor network
    :param url: the url to download
    :return: response
    """
    header = {'User-Agent': ua.random}
    web_page = requests.get(url, headers=header, proxies=proxies)
    return web_page


def extract_internal_links(web_page):
    request_url = web_page.request.url
    domain = urlparse(request_url).netloc

    # Make soup
    soup = BeautifulSoup(web_page.content, "html.parser", from_encoding="iso-8859-1")

    links_div = soup.find_all("div", {"class":{"row"}})[1]
    urls = set()

    
    # Get all internal links
    for a_tag in links_div.findAll("a"):
        
        href = a_tag.attrs.get("href")
        href = urljoin(request_url, href).strip("/")

        if href == "" or href is None:
            # href empty tag
            continue

        if urlparse(href).netloc != domain:
            # external link
            continue

        # print(href)
        web_page_in = send_tor_request(href)
        soup_in = BeautifulSoup(web_page_in.content, "html.parser", from_encoding="iso-8859-1")

        links_div_inside = soup_in.find_all("div", {"class":{"row"}})[1]
        
        if(len(links_div_inside.find_all("ul"))==0):
            print("skipped due to length 0")
            continue
      
        # print(links_div_inside.find_all("ul"))
        links_ul = links_div_inside.find("ul")
        

        for a_tag_inside in links_ul.find_all("a"):
            href_in = a_tag_inside.attrs.get("href")
            href_in = urljoin(request_url, href_in).strip("/")
            print(href_in) 
            print("")

            if href_in == "" or href_in is None:
                # href empty tag
                continue

            if urlparse(href_in).netloc != domain:
                # external link
                continue
            # print(href_in)
            urls.add(href_in)

    return list(urls)


if __name__ == '__main__':
    # Step 1: seed initialization
    seed = "http://xv3dbyx4iv35g7z2uoz2yznroy56oe32t7eppw2l2xvuel7km2xemrad.onion/store/nojs/index.php?route=product/category&path=80"

    web_page = send_tor_request(seed)
    links = extract_internal_links(web_page)

    print(links)

    for link in links:
        web_page = send_tor_request(link)
        time.sleep(2)
         # Save the page into the download folder
        filename = str(uuid.uuid4().hex) + ".html"
        path = os.path.join(resource_path, filename)
        with open(path, 'w', errors="ignore") as file:
            file.write(web_page.text)
        print(f"URL {link} saved under the name {filename}")


    # Step 2: creation of vivited list and queue (BFS)
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
    #         with open(path, 'w', errors="ignore") as file:
    #             file.write(web_page.text)
    #         print(f"URL {url} saved under the name {filename}")

    #         # Extract all the internal links
    #         new_urls = extract_internal_links(web_page)
    #         for new_url in new_urls:
    #             if new_url not in queue and new_url not in visited:
    #                 queue.append(new_url)