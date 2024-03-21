import threading
from tkinter import ttk, filedialog, messagebox

import customtkinter as ctk  # Import customtkinter instead of tkinter
from queue import Queue
from codeC.functiondirectory.display_threads import DisplayThreads
from codeC.functiondirectory.pdf import PDF_Generator2
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
        self.pdf_button = ctk.CTkButton(self, text="PDF", command=self.generate_pdf)  # Use CTkButton

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
        self.pdf_button.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        self.result_tree.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Creating a queue to store results from threads
        self.queue = Queue()
        self.list_pages = [Page()]
        self.page_audit_results = []
        self.th = threading.Thread

    def generate_pdf(self):
        PDF_Generator2.generate_pdf(self.page_audit_results)

    def start_audit(self):
        url = self.url_entry.get()
        self.page_audit_results.clear()
        if url:
            # self.start_button.configure(state='disabled')
            self.clear_results()
            display_thread = DisplayThreads(url=url, pages=self.list_pages, queue=self.queue, ihm=self)
            self.th = display_thread.start_thread()

    def clear_results(self):
        # Clear previous results from the Treeview
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

    def get_results(self):
        for page in self.list_pages:
            print(page.url)

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
        self.page_audit_results = []
        th = threading.Thread(target=self.update_result_tree)
        th.start()

    def update_ihm(self, result):
        # Create tags for different weight categories
        self.result_tree.tag_configure('high_weight',
                                       background='pink')  # Change 'pink' to any color you prefer for high weights
        self.result_tree.tag_configure('low_weight',
                                       background='lightgreen')  # Change 'lightgreen' to any color you prefer for low weights

        # Determine the display for the image weight based on its value and set the tag
        if result.image_weight:  # Check if there is an image weight value
            if result.image_weight > 100:
                image_weight_display = f"{round(result.image_weight, 2)} KB"
                weight_tag = 'high_weight'
            else:
                image_weight_display = f"{round(result.image_weight, 2)} KB"
                weight_tag = 'low_weight'
        else:
            # If there's no value, set to 'Unknown' and use default color
            image_weight_display = "Unknown"
            weight_tag = ''  # No tag applies default styling

        # Prepare the alt tags info
        alt_tags_info = f"{result.images_with_alt}"

        # Insert the row into the Treeview with the specified tag for color coding
        values = [
            result.url,
            result.load_time,
            result.h1,
            image_weight_display,  # Display for image weight
            round(result.video_size, 2) if result.video_size else 0,
            result.top_words,
            alt_tags_info,
            result.top_keywords  # Insert the top words and their frequencies
        ]

        val = {
            "Page" : result.url,
            'Temps de chargement' : result.load_time,
            'Présence H1' : result.h1,
        'Poids des images (KB)' : round(result.image_weight, 2) if result.image_weight else 0,
            'Taille des vidéos (KB)' : round(result.video_size, 2) if result.video_size else 0,
        'Top mots (fréquence)' : result.top_words,
        "Alt Tags" : alt_tags_info,
        "Top mots (pertinence)": result.top_keywords  # Insert the top words and their frequencies
        }
        self.page_audit_results.append(val)
        self.result_tree.insert("", "end", text=str(1), values=values, tags=(weight_tag,))


if __name__ == "__main__":
    app = AuditApp()
    app.mainloop()
