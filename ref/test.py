from queue import Queue

from codeC.functiondirectory.pc_ihm import Pc_IHM

main_url = 'https://profolio.eu/fr/'

file = Queue()

pc = Pc_IHM(file, url=main_url)

pc.start_thread()
