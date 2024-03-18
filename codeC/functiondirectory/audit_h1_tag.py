import threading

from bs4 import BeautifulSoup

from ref.page import Page


class AuditH1Tag(threading.Thread):
    h1 = ''
    p = Page()

    def __init__(self, html_content, p):
        super().__init__()
        self.html_content = html_content
        self.p = p

    def audit_h1_tags(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        h1_tags = soup.find_all('h1')
        return len(h1_tags)

    def run(self):
        self.h1 = self.audit_h1_tags()
        self.p.h1 = self.h1
        print("audit h1 : ", self.p.h1)

    def start_thread(self):
        th = AuditH1Tag(html_content=self.html_content, p=self.p)
        th.start()
        return th

    def get_load_time_and_content(self):
        return self.h1
