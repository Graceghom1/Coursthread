from queue import Queue
import threading
from codeC.functiondirectory.display_calc_threads import DisplayCalcThread
from ref.page import Page


class ConsumerLinks(threading.Thread):
    url = ''
    thread_calc_page = []
    pages_list = [Page]
    queue = Queue()
    queue_ihm = Queue()

    def __init__(self, queue, lock, queue_ihm):
        super().__init__()
        self.queue = queue
        self.pages_list = lock
        self.queue_ihm = queue_ihm

    def run(self):
        self.consume()

    def consume(self):
        while True:
            item = self.queue.get()
            # print("Consumer : ", item)
            if item == "END_LINKS":
                print("--------****** : ", item)
                break
            self.url = item
            p = DisplayCalcThread(item, self.pages_list, self.queue_ihm)
            p.start_thread()
            self.thread_calc_page.append(p)

    def start_thread(self):
        th = ConsumerLinks(queue=self.queue, lock=self.pages_list,  queue_ihm=self.queue_ihm)
        th.start()
        return th

    def get_th_children(self):
        return self.thread_calc_page
