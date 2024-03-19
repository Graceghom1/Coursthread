import threading
from bs4 import BeautifulSoup
from collections import Counter
import re
from ref.page import Page

class AuditWordFrequency(threading.Thread):
    def __init__(self, html_content, page):
        super().__init__()
        self.html_content = html_content
        self.page = page

    def audit_word_frequencies(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()
        # Get text and split into words
        text = soup.get_text()
        words = re.findall(r'\b\w+\b', text.lower())
        # Count the words
        count = Counter(words)
        # Select the top 5 most common words and their counts
        top_five = count.most_common(5)
        return top_five

    def run(self):
        top_five_words = self.audit_word_frequencies()
        # Convert the list of tuples into a string for display
        self.page.top_words = ', '.join([f'{word}: {freq}' for word, freq in top_five_words])
        print(f"Top words: {self.page.top_words}")

    def start_thread(self):
        th = AuditWordFrequency(html_content=self.html_content, page=self.page)
        th.start()
        return th
