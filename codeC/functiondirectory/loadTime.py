import threading
import time

import requests

from ref.page import Page


class LoadTimeAndContent(threading.Thread):
    load_time = ''
    html_content = ''
    p = Page()

    def __init__(self, url, p):
        super().__init__()
        self.url = url
        self.p = p

    def calculate_load_time(self):
        start_time = time.time()
        self.html_content = requests.get(self.url).content
        end_time = time.time()
        self.load_time = round(end_time - start_time, 3)
        return self.load_time, self.html_content

    def run(self):
        self.load_time, self.html_content = self.calculate_load_time()
        self.p.load_time = self.load_time
        print("run ", self.load_time)

    def start_thread(self):
        th = LoadTimeAndContent(url=self.url, p=self.p)
        th.start()
        return th

    def get_load_time_and_content(self):
        return self.load_time, self.html_content
