import threading
from queue import Queue

from codeC.functiondirectory.consumerLinks import ConsumerLinks
from codeC.functiondirectory.productLinks import ProductLinks


class DisplayThreads(threading.Thread):
    urlD = ''
    th_children = []
    lock = threading.Lock()

    def __init__(self, url, lock):
        super().__init__()
        self.urlD = url
        self.lock = lock

    def run(self):
        self.declaration()

    def declaration(self):
        file_attente = Queue()
        p = ProductLinks(url=self.urlD, queue=file_attente)
        th_p = p.start_thread()
        c = ConsumerLinks(queue=file_attente, lock=self.lock)
        th_c = c.start_thread()
        for th in th_c.get_th_children():
            print(th)
            th.join()

        th_p.join()
        th_c.join()

    def start_thread(self):
        th = DisplayThreads(self.urlD, self.lock)
        th.start()
        return th
