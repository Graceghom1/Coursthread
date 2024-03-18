import threading
from queue import Queue

from codeC.functiondirectory.consumerLinks import ConsumerLinks
from codeC.functiondirectory.productLinks import ProductLinks
from ref.page import Page


class DisplayThreads(threading.Thread):
    urlD = ''
    th_children = []
    list_pages = [Page()]
    queue = Queue()

    def __init__(self, url, pages, queue, ihm):
        super().__init__()
        self.urlD = url
        self.list_pages = pages
        self.queue = queue
        self.ihm=ihm

    def run(self):
        self.declaration()
        for l in self.list_pages:
            print("----------riadh : ***", l.url)

    def declaration(self):
        file_attente = Queue()
        p = ProductLinks(url=self.urlD, queue=file_attente)
        th_p = p.start_thread()
        c = ConsumerLinks(queue=file_attente, lock=self.list_pages, queue_ihm=self.queue, imh=self.ihm)
        th_c = c.start_thread()
        for th in th_c.get_th_children():
            print(th)
            th.join()

        th_p.join()
        th_c.join()

    def start_thread(self):
        th = DisplayThreads(self.urlD, self.list_pages, self.queue)
        th.start()
        return th
