import threading

import requests

from codeC.functiondirectory.audit_h1_tag import AuditH1Tag
from codeC.functiondirectory.loadTime import LoadTimeAndContent


class DisplayCalcThread(threading.Thread):

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        self.start_treatment_page()

    def start_treatment_page(self):
        print(self.url)
        __html = requests.get(self.url).content
        l = LoadTimeAndContent(self.url)
        th_load_time = l.start_thread()
        load_time, html_content = l.get_load_time_and_content()

        tag_h1 = AuditH1Tag(__html)
        th_tag_h1 = tag_h1.start_thread()

        th_load_time.join()
        th_tag_h1.join()

    def start_thread(self):
        th = DisplayCalcThread(self.url)
        th.start()
        return th
