import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from bs4 import BeautifulSoup
import base64
import urllib.parse
import time
import requests

from interface import WebCrawlerInterface


class AuditApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audit Web")

        self.crawler_gui = WebCrawlerInterface(root)

        self.crawler_gui.btn_audit.config(command=self.start_audit)

        # Création des widgets
        self.label_url = ttk.Label(root, text="URL à auditer:")
        self.entry_url = ttk.Entry(root, width=80)
        self.btn_audit = ttk.Button(root, text="Lancer l'audit", command=self.start_audit)
        self.text_results = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=40)

        # Positionnement des widgets dans la grille
        self.label_url.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_url.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.btn_audit.grid(row=0, column=2, padx=5, pady=5)
        self.text_results.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    def start_audit(self):
        # Fonction à exécuter lors du clic sur le bouton "Lancer l'audit"
        url = self.entry_url.get()
        url = self.crawler_gui.entry_url.get()
        keywords = self.crawler_gui.keywords_entry.get().split(",")

        self.crawler_gui.start_crawling(url, keywords)

        self.text_results.insert(tk.END, f"Auditing URL: {url}\n")
        self.audit_page(url)

    def get_html_content(self, url):
        response = requests.get(url)
        return response.content

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

    def audit_media_sizes(self, media_tags, media_type):
        for media_tag in media_tags:
            media_src = media_tag.get('src')
            media_size = self.get_image_size(media_src) if media_type == 'image' else self.get_video_size(media_src)
            if media_size:
                self.text_results.insert(tk.END,
                                         f"{media_type.capitalize()}: {media_src}, Taille: {media_size} octets\n")

    def audit_h1_tags(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        h1_tags = soup.find_all('h1')
        if h1_tags:
            self.text_results.insert(tk.END, "Les balises <h1> sont présentes sur la page.\n")
        else:
            self.text_results.insert(tk.END, "Attention : Aucune balise <h1> n'a été trouvée sur la page.\n")

    def audit_keywords(self, html_content, mots_cles):
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text().lower()
        for mot_cle in mots_cles:
            if mot_cle.lower() in text:
                self.text_results.insert(tk.END, f"Le mot-clé '{mot_cle}' est présent sur la page.\n")
            else:
                self.text_results.insert(tk.END,
                                         f"Attention : Le mot-clé '{mot_cle}' n'a pas été trouvé sur la page.\n")

    def calculate_load_time(self, url):
        start_time = time.time()
        self.get_html_content(url)
        end_time = time.time()
        load_time = end_time - start_time
        self.text_results.insert(tk.END, f"Temps de chargement de {url}: {load_time} secondes\n")

    def check_alt_tags(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            if not img_tag.get('alt'):
                self.text_results.insert(tk.END, "Attention : Balise 'alt' manquante pour une image.\n")

    def detect_copy_paste(self, html_content):
        pass

    def audit_page(self, url):
        html_content = self.get_html_content(url)
        self.calculate_load_time(url)
        img_tags, video_tags = self.extract_media_tags(html_content)
        self.audit_media_sizes(img_tags, 'image')
        self.audit_media_sizes(video_tags, 'video')
        self.audit_h1_tags(html_content)
        self.audit_keywords(html_content, ['mot_cle_1', 'mot_cle_2', 'mot_cle_3'])
        self.check_alt_tags(html_content)
        self.detect_copy_paste(html_content)

    def __init__(self, root):
        self.root = root
        self.root.title("Audit App")

        self.crawler_gui = WebCrawlerInterface(root)


if __name__ == "__main__":
    root = tk.Tk()
    app = AuditApp(root)
    root.mainloop()
