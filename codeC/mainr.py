from queue import Queue

from codeC.functiondirectory.display_threads import DisplayThreads

main_url = 'https://www.facebook.com/'
# main_url = 'https://profolio.eu/fr/'

disp = DisplayThreads(main_url)
disp.start_thread()
