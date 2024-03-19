import queue
import threading
from queue import Queue

import requests

from codeC.functiondirectory.alt_images import AltImages
from codeC.functiondirectory.audit_h1_tag import AuditH1Tag
from codeC.functiondirectory.loadTime import LoadTimeAndContent
from ref.page import Page


class DisplayCalcThread(threading.Thread):
    pages = [Page()]
    file_queue = queue.Queue()

    def __init__(self, url, lock, f_queue, ihm):
        super().__init__()
        self.url = url
        self.pages = lock
        self.file_queue = f_queue
        self.ihm = ihm

    def run(self):
        p = self.start_treatment_page()
        self.ihm.update_ihm(p)

    def start_treatment_page(self):
        p = Page()
        print(self.url)
        p.url = self.url
        __html = requests.get(self.url).content
        l = LoadTimeAndContent(self.url, p)
        th_load_time = l.start_thread()
        load_time, html_content = l.get_load_time_and_content()

        tag_h1 = AuditH1Tag(__html, p)
        th_tag_h1 = tag_h1.start_thread()

        alt_th = AltImages(html_content=__html, p=p)
        th_alt = alt_th.start_thread()

        th_load_time.join()
        th_tag_h1.join()
        th_alt.join()
        self.file_queue.put(p)

        return p

    def start_thread(self):
        th = DisplayCalcThread(self.url, self.pages, self.file_queue, self.ihm)
        th.start()
        return th
