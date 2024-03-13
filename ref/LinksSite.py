import threading
from queue import Queue

import requests
import time

from bs4 import BeautifulSoup

import urllib.parse


class LinkSite(threading.Thread):
    links = []
    links_outgoing = []
    file_attente = Queue()

    url = ""

    def run(self):
        self.extract_links(self.url)
        self.file_attente.put("END_LINKS")

    def base_url(self, url, with_path=False):
        parsed = urllib.parse.urlparse(url)
        path = '/'.join(parsed.path.split('/')[:-1]) if with_path else ''
        parsed = parsed._replace(path=path)
        parsed = parsed._replace(params='')
        parsed = parsed._replace(query='')
        parsed = parsed._replace(fragment='')
        return parsed.geturl()

    def extract_links(self, url):
        url_base = self.base_url(url)
        source_url = requests.get(url)
        soup = BeautifulSoup(source_url.content, "html.parser")
        for link in soup.find_all('a', href=True):
            try:
                jpg_link = (link.get('href').find(".jpg") > -1)
                png_link = (link.get('href').find(".png") > -1)
                if link.get('href').startswith(url_base) and not jpg_link and not png_link and link.get(
                        "href") not in self.links:
                    self.links.append(link.get('href'))
                    self.file_attente.put(link.get('href'))
                    self.extract_links(link.get('href'))
                else:
                    if not link.get('href').startswith(url_base) and link.get('href').startswith(
                            "http") and not jpg_link and not png_link and link.get("href") not in self.links_outgoing:
                        self.links_outgoing.append(link.get('href'))
                        # print("source url outgoing", link.get('href'))

            except Exception as e:
                print("Unhandled exception", e)
