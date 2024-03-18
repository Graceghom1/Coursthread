from queue import Queue
import threading
from codeC.functiondirectory.display_calc_threads import DisplayCalcThread


class ConsumerLinks(threading.Thread):
    url = ''
    thread_calc_page = []
    lock = threading.Lock()
    queue = Queue()

    def __init__(self, queue, lock):
        super().__init__()
        self.queue = queue
        self.lock = lock

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
            # self.lock.acquire()
            p = DisplayCalcThread(item, self.lock)
            p.start_thread()
            self.thread_calc_page.append(p)

    def start_thread(self):
        th = ConsumerLinks(queue=self.queue, lock=self.lock)
        th.start()
        return th

    def get_th_children(self):
        return self.thread_calc_page
