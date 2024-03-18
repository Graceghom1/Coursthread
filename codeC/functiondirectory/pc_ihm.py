import threading
from queue import Queue

from codeC.functiondirectory.display_threads import DisplayThreads
from ref.page import Page


class Pc_IHM(threading.Thread):
    queue = Queue()
    url = ""
    list_pages = [Page()]

    def __init__(self, queue, url):
        super().__init__()
        self.queue = queue
        self.url = url

    def run(self):
        self.declaration()


    def declaration(self):
        p = DisplayThreads(url=self.url, queue=Queue, pages=self.list_pages)
        p.start_thread()

        self.consume()

        # p = self.queue.get()
        # print("consommateur ---- // -- ** : ", p.url)

    def consume(self):
        while True:
            item = self.queue.get()
            print("consommateur ---- // -- ** : ", item.url)

    def start_thread(self):
        th = Pc_IHM(queue=self.queue, url=self.url)
        th.start()
        th.join()
