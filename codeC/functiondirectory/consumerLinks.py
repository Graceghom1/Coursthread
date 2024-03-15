import queue
import threading
from codeC.functiondirectory.display_calc_threads import DisplayCalcThread


class ConsumerLinks(threading.Thread):
    url = ''
    thread_calc_page = []

    def __init__(self, queue=None):
        super().__init__()
        if queue is None:
            pass
        else:
            self.queue = queue

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
            p = DisplayCalcThread(item)
            p.start_thread()
            self.thread_calc_page.append(p)

    def start_thread(self):
        th = ConsumerLinks(queue=self.queue)
        th.start()
        return th

    def get_th_children(self):
        return self.thread_calc_page
