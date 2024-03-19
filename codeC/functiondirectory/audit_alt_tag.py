import threading
from bs4 import BeautifulSoup
from ref.page import Page


class AuditAltTags(threading.Thread):
    def __init__(self, html_content, page):
        super().__init__()
        self.html_content = html_content
        self.page = page

    def audit_alt_tags(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        images = soup.find_all('img')
        total_images = len(images)
        images_with_alt = sum(1 for img in images if img.get('alt') is not None)
        # Return the count of images with and without alt attributes
        return total_images, images_with_alt

    def run(self):
        total_images, images_with_alt = self.audit_alt_tags()
        # Store the counts in the page object
        self.page.total_images = total_images
        self.page.images_with_alt = images_with_alt
        print(f"Images with alt tags: {self.page.images_with_alt}/{self.page.total_images}")

    def start_thread(self):
        th = AuditAltTags(html_content=self.html_content, page=self.page)
        th.start()
        return th
