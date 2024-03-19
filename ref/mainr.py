import queue
import threading
import tkinter
from queue import Queue

from codeC.functiondirectory.display_threads import DisplayThreads
from ref.page import Page

main_url = 'https://www.facebook.com/'

# main_url = 'https://profolio.eu/fr/'

lock = [Page]
qq = queue.Queue()


def lancer():
    url = url_name_entry.get()
    if url:
        disp = DisplayThreads(url, lock, queue=qq)
        th = disp.start_thread()
        th.join()


# debut de IHM
window = tkinter.Tk()
window.title("Audite site internet")

frame = tkinter.Frame(window)
frame.pack()

# Site information
url_info_frame = tkinter.LabelFrame(frame, text="URL Information")
url_info_frame.grid(row=0, column=0, padx=40, pady=20)
url_name_label = tkinter.Label(url_info_frame, text="URL SITE")
url_name_label.grid(row=0, column=0)
url_name_entry = tkinter.Entry(url_info_frame)
url_name_entry.grid(row=1, column=0)

# Cretere de recerche

cr_frame = tkinter.LabelFrame(frame)
cr_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

cr1_label = tkinter.Label(cr_frame, text="Mot clé 1 : ")
cr1_label.grid(row=0, column=0)
cr1_name_entry = tkinter.Entry(cr_frame)
cr1_name_entry.grid(row=0, column=1)

cr2_label = tkinter.Label(cr_frame, text="Mot clé 2 : ")
cr2_label.grid(row=1, column=0)
cr2_name_entry = tkinter.Entry(cr_frame)
cr2_name_entry.grid(row=1, column=1)

cr3_label = tkinter.Label(cr_frame, text="Mot clé 2 : ")
cr3_label.grid(row=2, column=0)
cr3_name_entry = tkinter.Entry(cr_frame)
cr3_name_entry.grid(row=2, column=1)

for widget in cr_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Button
button = tkinter.Button(frame, text="Lancer ...", command=lancer)
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

window.mainloop()
