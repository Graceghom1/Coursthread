import threading
from queue import Queue

from codeC.functiondirectory.consumerLinks import ConsumerLinks
from codeC.functiondirectory.productLinks import ProductLinks


class DisplayThreads(threading.Thread):
    urlD = ''
    th_children = []

    def __init__(self, url, gui):
        super().__init__()
        self.url = url
        self.gui = gui
        self.results = []

    def run(self):
        self.declaration()

    def declaration(self):
        file_queue = Queue()
        producer = ProductLinks(url=self.url, queue=file_queue)
        producer_thread = producer.start_thread()

        consumer = ConsumerLinks(queue=file_queue)
        consumer_thread = consumer.start_thread()

        for thread in consumer.get_th_children():
            thread.join()
            self.results.append(thread.get_result())

        producer_thread.join()
        consumer_thread.join()

        # Afficher les résultats dans l'interface graphique
        self.gui.display_results(self.results)

    # def start_thread(self):
    #     th = DisplayThreads()
    #     th.start()
    #     th.join()

    def start_thread(self):
        th = DisplayThreads(self.urlD, self.gui)
        th.start()
        th.join()
