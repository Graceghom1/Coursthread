import queue
import threading
from queue import Queue

import requests

from codeC.functiondirectory.audit_alt_tag import AuditAltTags
from codeC.functiondirectory.audit_h1_tag import AuditH1Tag
from codeC.functiondirectory.audit_image_weight import AuditImageWeight
from codeC.functiondirectory.audit_video import AuditVideoSize
from codeC.functiondirectory.audit_word_frequency import AuditWordFrequency
from codeC.functiondirectory.audit_word_pertinence import AuditWordPertinence
from codeC.functiondirectory.loadTime import LoadTimeAndContent
from ref.page import Page


class DisplayCalcThread(threading.Thread):
    pages = [Page()]
    file_queue = queue.Queue()

    def __init__(self, url, lock, f_queue, ihm):
        super().__init__()
        self.url = url
        self.pages = lock
        self.file_queue = f_queue
        self.ihm = ihm

    def run(self):
        p = self.start_treatment_page()
        self.ihm.update_ihm(p)

    def start_treatment_page(self):
        p = Page()
        print(self.url)
        p.url = self.url
        html_content = requests.get(self.url).content

        # Load time and content
        load_time_and_content = LoadTimeAndContent(self.url, p)
        th_load_time = load_time_and_content.start_thread()

        # H1 tag audit
        audit_h1 = AuditH1Tag(html_content, p)
        th_tag_h1 = audit_h1.start_thread()

        # Image weight audit
        audit_images = AuditImageWeight(html_content, p)
        th_images = audit_images.start_thread()

        # New video size audit
        audit_videos = AuditVideoSize(html_content, p)
        th_videos = audit_videos.start_thread()

        # Existing audits
        audit_words = AuditWordFrequency(html_content, p)
        th_words = audit_words.start_thread()

        # Audit for alt tags
        audit_alt = AuditAltTags(html_content, p)
        th_alt = audit_alt.start_thread()

        # Start the word pertinence audit
        audit_word_pertinence = AuditWordPertinence(html_content, p)
        th_word_pertinence = audit_word_pertinence.start_thread()

        # Wait for all threads to complete
        th_load_time.join()
        th_tag_h1.join()
        th_images.join()
        th_videos.join()
        th_words.join()
        th_alt.join()
        th_word_pertinence.join()
        
        # Put the page into the queue for later use
        self.file_queue.put(p)

        return p

    def start_thread(self):
        th = DisplayCalcThread(self.url, self.pages, self.file_queue, self.ihm)
        th.start()
        return th
