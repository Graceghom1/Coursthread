import threading

import requests
from bs4 import BeautifulSoup

from ref.page import Page


class AltImages(threading.Thread):
    p = Page()
    presence_alt = False

    def __init__(self, html_content, p):
        super().__init__()
        self.html_content = html_content
        self.p = p

    def has_alt_attribute(self, img):
        return "alt" in img.attrs

    def presence_alt_image(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        images = soup.find_all('img')
        for image in images:
            if not self.has_alt_attribute(image):
                self.presence_alt = False
                return False

        self.presence_alt = True
        return True

    def run(self):
        ok = self.presence_alt_image()
        self.p.img_tags = self.presence_alt
        print("/////////////----------------", ok)

    def start_thread(self):
        th = AltImages(html_content=self.html_content, p=self.p)
        th.start()
        return th