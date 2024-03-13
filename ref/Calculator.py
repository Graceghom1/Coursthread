import threading

from bs4 import BeautifulSoup
import base64
import urllib.parse
import time
import requests

from ref.page import Page


def get_html_content(url):
    response = requests.get(url)
    return response.content


class Calculator:
    page_url = Page

    verrou = threading.Lock()

    def __init__(self, url):
        self.url = url

    def calculate_load_time(self):
        self.verrou.acquire()
        try:
            start_time = time.time()
            get_html_content(self.url)
            end_time = time.time()
            load_time = end_time - start_time
        finally:
            self.verrou.release()
        return load_time

    def extract_media_tags(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        img_tags = soup.find_all('img')
        video_tags = soup.find_all('video')
        return img_tags, video_tags

    def get_image_size(self, image_src):
        if image_src.startswith('data:image'):
            return self.get_base64_image_size(image_src.split(',')[1])
        else:
            try:
                with urllib.request.urlopen(image_src) as response:
                    return response.length
            except Exception as e:
                print(f"Erreur lors de la récupération de la taille de l'image {image_src}: {e}")
                return None

    def get_base64_image_size(self, base64_data):
        try:
            image_data = base64.b64decode(base64_data)
            image_size = len(image_data)
            return image_size
        except Exception as e:
            print(f"Erreur lors de la récupération de la taille de l'image encodée en base64: {e}")
            return None

    def get_video_size(self, video_url):
        try:
            with urllib.request.urlopen(video_url) as response:
                return response.length
        except Exception as e:
            print(f"Erreur lors de la récupération de la taille de la vidéo {video_url}: {e}")
            return None

    def audit_h1_tags(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        h1_tags = soup.find_all('h1')
        return len(h1_tags)

    def detect_copy_paste(self, html_content):
        pass

    def audit_page(self):
        self.page_url.load_time = self.calculate_load_time()
        html_content = get_html_content(self.url)
        self.page_url.img_tags, self.page_url.video_tags = self.extract_media_tags(html_content)
        self.page_url.h1 = self.audit_h1_tags(html_content)
        self.detect_copy_paste(html_content)
