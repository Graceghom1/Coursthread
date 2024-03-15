import threading

from bs4 import BeautifulSoup


class AuditH1Tag(threading.Thread):
    h1 = ''

    def __init__(self, html_content):
        super().__init__()
        self.html_content = html_content

    def audit_h1_tags(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        h1_tags = soup.find_all('h1')
        return len(h1_tags)

    def run(self):
        self.h1= self.audit_h1_tags()
        print("audit h1 : ", self.h1)

    def start_thread(self):
        th = AuditH1Tag(html_content=self.html_content)
        th.start()
        return th

    def get_load_time_and_content(self):
        return self.h1
