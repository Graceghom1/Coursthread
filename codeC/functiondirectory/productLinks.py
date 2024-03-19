import threading
from queue import Queue
import requests
from bs4 import BeautifulSoup
import urllib.parse
from collections import deque


class ProductLinks(threading.Thread):
    links = []
    links_outgoing = []
    file_queue = Queue()

    url = ""

    def __init__(self, url, queue):
        super().__init__()
        self.url = url
        self.file_queue = queue

    def run(self):
        # self.extract_links(self.url)
        self.get_links(self.url, 1)
        self.file_queue.put("END_LINKS")

    def start_thread(self):
        th = ProductLinks(url=self.url, queue=self.file_queue)
        th.start()
        return th

    def base_url(self, url, with_path=False):
        parsed = urllib.parse.urlparse(url)
        path = '/'.join(parsed.path.split('/')[:-1]) if with_path else ''
        parsed = parsed._replace(path=path)
        parsed = parsed._replace(params='')
        parsed = parsed._replace(query='')
        parsed = parsed._replace(fragment='')
        return parsed.geturl()

    def get_links(self, url, max_depth):
        visited = set()
        url_base = self.base_url(url)
        queue = deque([(url, 0)])  # Initialize a queue with the starting URL and depth 0
        while queue:
            current_url, depth = queue.popleft()
            if depth > max_depth or current_url in visited:
                continue

            try:
                if current_url.startswith('/'):
                    current_url = url_base + current_url
                if current_url.startswith(url_base) and current_url not in visited:
                    response = requests.get(current_url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    links = [link.get('href') for link in soup.find_all('a', href=True)]
                    # print("Links on", .)
                    self.file_queue.put(current_url)
                    visited.add(current_url)
                    for link in links:
                        queue.append((link, depth + 1))
                else :
                    self.links_outgoing.append(current_url)
            except Exception as e:
                print('', e)

    def extract_links(self, url):
        print("URL de BASE : ", url)
        url_base = self.base_url(url)
        source_url = requests.get(url)
        soup = BeautifulSoup(source_url.content, "html.parser")
        for link in soup.find_all('a', href=True):
            try:
                jpg_link = (link.get('href').find(".jpg") > -1)
                png_link = (link.get('href').find(".png") > -1)
                pdf_link = (link.get('href').find(".pdf") > -1)
                if link.get('href').startswith('http') and not jpg_link and not pdf_link and not png_link and link.get(
                        "href") not in self.links:
                    self.links.append(link.get('href'))
                    self.file_queue.put(link.get('href'))
                    self.extract_links(link.get('href'))
                else:
                    if not link.get('href').startswith(url_base) and link.get('href').startswith(
                            "http") and not jpg_link and not pdf_link and not png_link and link.get("href") not in self.links_outgoing:
                        self.links_outgoing.append(link.get('href'))
                        # print("1111111111111111 *************** ", link.get('href'))

            except Exception as e:
                print("Unhandled exception", e)
