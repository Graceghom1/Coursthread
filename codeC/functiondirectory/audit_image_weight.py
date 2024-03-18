import threading
import requests
from bs4 import BeautifulSoup
from ref.page import Page


class AuditImageWeight(threading.Thread):
    def __init__(self, html_content, page):
        super().__init__()
        self.html_content = html_content
        self.page = page
        self.image_weights = []  # To store the size of each image

    def audit_image_weights(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        images = soup.find_all('img')
        total_weight = 0
        for img in images:
            # Extract the image source URL
            src = img.get('src')
            if src:
                # Ensure the URL is absolute
                response = requests.get(src, stream=True)
                # Calculate the image size in kilobytes (1 kilobyte = 1024 bytes)
                size = len(response.content) / 1024
                self.image_weights.append(size)
                total_weight += size
        return total_weight

    def run(self):
        total_weight = self.audit_image_weights()
        # Store the total weight of all images on the page
        self.page.image_weight = total_weight
        print(f"Total image weight: {self.page.image_weight}KB")

    def start_thread(self):
        th = AuditImageWeight(html_content=self.html_content, page=self.page)
        th.start()
        return th
