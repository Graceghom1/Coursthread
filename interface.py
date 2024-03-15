import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class WebCrawlerInterface:
    def __init__(self, root):
        self.root = root

        self.url_label = ttk.Label(root, text="URL:")
        self.url_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        self.keywords_label = ttk.Label(root, text="Mots-clés:")
        self.keywords_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.keywords_entry = ttk.Entry(root, width=50)
        self.keywords_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        self.crawl_button = ttk.Button(root, text="Crawler", command=self.start_crawling)
        self.crawl_button.grid(row=2, column=1, padx=5, pady=5)

        self.result_table = ttk.Treeview(root, columns=("Pages", "Mots-clés", "Temps d'exécution"))
        self.result_table.heading("#0", text="")
        self.result_table.heading("Pages", text="Pages")
        self.result_table.heading("Mots-clés", text="Mots-clés")
        self.result_table.heading("Temps d'exécution", text="Temps d'exécution")
        self.result_table.column("#0", width=1)
        self.result_table.column("Pages", width=200)
        self.result_table.column("Mots-clés", width=200)
        self.result_table.column("Temps d'exécution", width=150)
        self.result_table.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.root.rowconfigure(3, weight=1)
        self.root.columnconfigure(1, weight=1)

    def start_crawling(self, url, keywords):
        url = self.url_entry.get()
        keywords = self.keywords_entry.get().split(",")

        start_time = time.time()
        unique_links = self.get_unique_links(url)
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)

        self.result_table.insert("", "end", text="", values=(url, ", ".join(keywords), f"{execution_time} s"))

        if not url:
            messagebox.showerror("Erreur", "Veuillez saisir une URL.")
            return
        if not keywords:
            messagebox.showerror("Erreur", "Veuillez saisir au moins un mot-clé.")
            return

        threading.Thread(target=self.crawl_url, args=(url, keywords)).start()

    def crawl_url(self, url, keywords):
        start_time = time.time()
        unique_links = self.get_unique_links(url)
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)

        for link in unique_links:
            self.result_table.insert("", "end", text="", values=(link, ", ".join(keywords), f"{execution_time} s"))

    def get_unique_links(self, url):
        unique_links = set()
        visited_links = set()
        links_to_visit = set([url])

        while links_to_visit:
            current_url = links_to_visit.pop()

            if current_url in visited_links:
                continue

            visited_links.add(current_url)

            response = requests.get(current_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                page_links = soup.find_all('a')

                for link in page_links:
                    href = link.get('href')
                    if href and href.startswith('http'):
                        absolute_url = urljoin(current_url, href)
                        unique_links.add(absolute_url)
                        if absolute_url not in visited_links:
                            links_to_visit.add(absolute_url)

        return unique_links

    # if __name__ == "__main__":
    #     root = tk.Tk()
    #     app = AuditApp(root)
    #     root.mainloop()

