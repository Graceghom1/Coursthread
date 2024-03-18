import threading
import tkinter as tk
from tkinter import ttk
from queue import Queue
from codeC.functiondirectory.display_threads import DisplayThreads
from ref.page import Page


class AuditApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audit Web")

        # Création des widgets
        self.url_label = ttk.Label(self, text="URL:")
        self.url_entry = ttk.Entry(self, width=50)
        self.start_button = ttk.Button(self, text="Lancer l'audit", command=self.start_audit)

        # Création du Treeview pour afficher les résultats
        self.result_tree = ttk.Treeview(self, columns=("Page", "Temps de chargement", "Présence H1"))
        self.result_tree.heading("Page", text="Page")
        self.result_tree.heading("Temps de chargement", text="Temps de chargement")
        self.result_tree.heading("Présence H1", text="Présence H1")

        # Positionnement des widgets dans la grille
        self.url_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.start_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.result_tree.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Création d'une file d'attente pour stocker les résultats des threads
        self.queue = Queue()
        self.list_pages = [Page()]

    def start_audit(self):
        url = self.url_entry.get()
        if url:
            self.clear_results()
            display_thread = DisplayThreads(url=url, pages=self.list_pages, queue=self.queue, ihm=self)
            display_thread.start()


    def clear_results(self):
        # Effacer les résultats précédents du Treeview
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

    def update_result_tree(self):
        print("JE suis Exterier ")
        # Afficher les résultats dans le Treeview
        while True:  # while not self.queue.empty():
            print("JE suis la interieure ")
            result = self.queue.get()
            print("Je suis interface ///-------", result.url)
            self.result_tree.insert("", "end", text=str(1), values=[result.url, result.load_time, result.h1])
            # for idx, item in enumerate(result, start=1):
            #     self.result_tree.insert("", "end", text=str(idx), values=item)

        # Rappeler cette méthode périodiquement
        # self.after(1000, self.update_result_tree)

    def display_results(self, results):
        # Mettre les résultats dans la file d'attente pour affichage
        self.queue.put(results)

    def lancer_th_maj(self):
        print("JE suis la ")
        th = threading.Thread(target=self.update_result_tree)
        th.start()

    def update_ihm(self, result):
        self.result_tree.insert("", "end", text=str(1), values=[result.url, result.load_time, result.h1])


if __name__ == "__main__":
    app = AuditApp()
    app.mainloop()
