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


#resource_path = 'resources/pds' # REPLACE WITH YOUR HTML FOLDER PATH

crawler_dictionary = {'resources/pds': "http://4p6i33oqj6wgvzgzczyqlueav3tz456rdu632xzyxbnhq4gpsriirtqd.onion/",
                      'resources/BitPharma':"http://7bw24ll47y7aohhkrfdq2wydg3zvuecvjo63muycjzlbaqlihuogqvyd.onion/",
                      'resources/CanUK':'http://hyxme2arc5jnevzlou547w2aaxubjm7mxhbhtk73boiwjxewawmrz6qd.onion/',
                      'resources/Smokeables':'http://porf65zpwy2yo4sjvynrl4eylj27ibrmo5s2bozrhffie63c7cxqawid.onion/',
                      'resources/EuCanna':'http://wges3aohuplu6he5tv4pn7sg2qaummlokimim6oaauqo2l7lbx4ufyyd.onion/',
                      'resources/DeDope':'http://dumlq77rikgevyimsj6e2cwfsueo7ooynno2rrvwmppngmntboe2hbyd.onion/',
                      'resources/BrainMagic':'http://6hzbfxpnsdo4bkplp5uojidkibswevsz3cfpdynih3qvfr24t5qlkcyd.onion/',
                      'resources/NLGrowers':'http://gn74rz534aeyfxqf33hqg6iuspizulmvpd7zoyz7ybjq4jo3whkykryd.onion/',
                      'resources/MidlandCity':'http://mcityef3eueeh26mo2e7jn6yypgnvtbu2w57kcka6g3zu7u4xv5cgkid.onion/'}

def send_tor_request(url):Forensics
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
    for resource_path, seed in crawler_dictionary.items():
        #seed = "http://4p6i33oqj6wgvzgzczyqlueav3tz456rdu632xzyxbnhq4gpsriirtqd.onion/"

        # Step 2: creation of visited list and queue (BFS)
        visited = set()
        queue = deque()

        # Step 3: add the seed to the queue
        queue.append(seed)

        # Step 4: Iterate over the queue until it's empty
        exit_condition_max_links = 20
        while queue and len(visited) < exit_condition_max_links:
            url = queue.popleft()

            if url not in visited:
                # Send tor request to download the page
                web_page = send_tor_request(url)
                time.sleep(2)

                # Update the visited pages
                visited.add(url)

                # Save the page into the download folder
                filename = str(uuid.uuid4().hex) + ".html"
                path = os.path.join(resource_path, filename)
                with open(path, 'w') as file:
                    file.write(web_page.text)
                print(f"URL {url} saved under the name {filename}")

                # Extract all the internal links
                new_urls = extract_internal_links(web_page)
                for new_url in new_urls:
                    if new_url not in queue and new_url not in visited:
                        queue.append(new_url)