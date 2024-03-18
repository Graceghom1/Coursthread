import threading
from tkinter import ttk

import customtkinter as ctk  # Import customtkinter instead of tkinter
from queue import Queue
from codeC.functiondirectory.display_threads import DisplayThreads
from ref.page import Page


class AuditApp(ctk.CTk):  # Inherit from CTk instead of tk.Tk
    def __init__(self):
        super().__init__()
        self.title("Audit Web")

        # Creating widgets using customtkinter
        self.url_label = ctk.CTkLabel(self, text="URL:")  # Use CTkLabel
        self.url_entry = ctk.CTkEntry(self,
                                      width=400)  # Use CTkEntry, note that the width is different in customtkinter
        self.start_button = ctk.CTkButton(self, text="Lancer l'audit", command=self.start_audit)  # Use CTkButton

        # Creating the Treeview for displaying results
        # Note: customtkinter doesn't provide a direct replacement for Treeview,
        # so we'll keep using the ttk.Treeview for now.
        # If you need a matching style, you may need to customize ttk.Treeview or use a different approach.
        self.result_tree = ttk.Treeview(self, columns=(
            "Page", "Temps de chargement", "Présence H1", "Poids des images", "Taille des vidéos", "Top mots",
            "Alt Tags",
            "Top keywords"))

        self.result_tree.heading("Page", text="Page")
        self.result_tree.heading("Temps de chargement", text="Temps de chargement")
        self.result_tree.heading("Présence H1", text="Présence H1")
        self.result_tree.heading("Poids des images", text="Poids des images (KB)")  # New column for image weights
        self.result_tree.heading("Taille des vidéos", text="Taille des vidéos (KB)")
        self.result_tree.heading("Top mots", text="Top mots (fréquence)")
        self.result_tree.heading("Alt Tags", text="Alt Tags")
        self.result_tree.heading("Top keywords", text="Top mots (pertinence)")

        self.result_tree.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        # Allow the second row (index 2, where your Treeview is placed) to expand
        self.grid_rowconfigure(2, weight=1)

        # Allow the columns to expand; assuming you have 2 columns as indicated by columnspan=2
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Positioning widgets using grid
        self.url_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.start_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.result_tree.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Creating a queue to store results from threads
        self.queue = Queue()
        self.list_pages = [Page()]

    def start_audit(self):
        url = self.url_entry.get()
        if url:
            self.clear_results()
            display_thread = DisplayThreads(url=url, pages=self.list_pages, queue=self.queue, ihm=self)
            display_thread.start()

    def clear_results(self):
        # Clear previous results from the Treeview
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

    def update_result_tree(self):
        # Display results in the Treeview
        while not self.queue.empty():
            result = self.queue.get()
            self.result_tree.insert("", "end", text=str(1), values=[result.url, result.load_time, result.h1])
            # In a real scenario, remove the infinite loop and use self.after to schedule updates

    def display_results(self, results):
        # Queue results for display
        self.queue.put(results)

    def lancer_th_maj(self):
        th = threading.Thread(target=self.update_result_tree)
        th.start()

    def update_ihm(self, result):
        alt_tags_info = f"{result.images_with_alt}"
        self.result_tree.insert("", "end", text=str(1), values=[
            result.url,
            result.load_time,
            result.h1,
            round(result.image_weight, 2) if result.image_weight else 0,
            round(result.video_size, 2) if result.video_size else 0,
            result.top_words,
            alt_tags_info,
            result.top_keywords  # Insert the top words and their frequencies
        ])


if __name__ == "__main__":
    app = AuditApp()
    app.mainloop()
