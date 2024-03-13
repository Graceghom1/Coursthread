#
# # start_url = 'https://www.scrapingbee.com/blog/crawling-python/'
#
# extract_links(start_url)
#
# for link in links_outgoing:
#     print(link)
import threading
from queue import Queue

from ref.Calculator import Calculator
from ref.LinksSite import LinkSite
from ref.page import Page

threads = []
pages = []
verrou = threading.Lock()
verrouth = threading.Lock()


def function_consumer():
    global threads
    while True:
        item = links_intra.get()
        if item == "END_LINKS":
            print("--------****** : ", item)
            break
        verrouth.acquire()
        p = threading.Thread(target=page_url, args=(item,))
        p.start()
        threads.append(p)
        # print("consomateur file Attente ", item)


def page_url(url):
    print("-------------START------------------")
    print("affichage 1 " + url)
    cal = Calculator(url)
    p = Page
    p.url = url
    cal.page_url = p
    cal.verrou = verrou
    cal.audit_page()
    pages.append(p)
    print(p.load_time)
    print("affichage 2 " + p.url)
    print("--------------END-----------------")
    verrouth.release()


links_intra = Queue()
start_url = 'https://profolio.eu/'

getLinkSite = LinkSite()
getLinkSite.file_attente = links_intra
getLinkSite.url = start_url

consomme = threading.Thread(target=function_consumer)

getLinkSite.start()
consomme.start()

consomme.join()

getLinkSite.join()

for th in threads:
    th.join()

