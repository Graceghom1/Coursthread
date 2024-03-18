import threading
import requests
from bs4 import BeautifulSoup
from ref.page import Page


class AuditVideoSize(threading.Thread):
    def __init__(self, html_content, page):
        super().__init__()
        self.html_content = html_content
        self.page = page
        self.video_sizes = []  # Store the size of each video

    def audit_video_sizes(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        videos = soup.find_all('video')
        total_size = 0
        for video in videos:
            # Extract the video source URL
            # Assuming the source is directly within the video tag as a source child
            for source in video.find_all('source'):
                src = source.get('src')
                if src:
                    response = requests.get(src, stream=True)
                    # Calculate the video size in kilobytes
                    size = len(response.content) / 1024
                    self.video_sizes.append(size)
                    total_size += size
        return total_size

    def run(self):
        total_size = self.audit_video_sizes()
        # Store the total size of all videos on the page
        self.page.video_size = total_size
        print(f"Total video size: {self.page.video_size}KB")

    def start_thread(self):
        th = AuditVideoSize(html_content=self.html_content, page=self.page)
        th.start()
        return th
