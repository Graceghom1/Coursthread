import threading
from queue import Queue

from codeC.functiondirectory.consumerLinks import ConsumerLinks
from codeC.functiondirectory.productLinks import ProductLinks


class DisplayThreads(threading.Thread):
    urlD = ''
    th_children = []

    def __init__(self, url):
        super().__init__()
        self.urlD = url

    def run(self):
        self.declaration()

    def declaration(self):
        file_attente = Queue()
        producteur = ProductLinks(url=self.urlD, queue=file_attente)
        th_p = producteur.start_thread()
        consommateur = ConsumerLinks(queue=file_attente)
        th_c = consommateur.start_thread()
        for th in th_c.get_th_children():
            th.join()

        th_p.join()
        th_c.join()

    def start_thread(self):
        th = DisplayThreads(self.urlD)
        th.start()
        th.join()
