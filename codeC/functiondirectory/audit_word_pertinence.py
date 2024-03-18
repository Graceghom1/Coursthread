import nltk

nltk.download('stopwords')

import threading

import nltk
from bs4 import BeautifulSoup
from collections import Counter
import re
from ref.page import Page
from nltk.corpus import stopwords

# Set up stop words for English (or replace 'english' with the needed language)
STOP_WORDS = set(stopwords.words('english')) | set(stopwords.words('french'))


class AuditWordPertinence(threading.Thread):
    def __init__(self, html_content, page):
        super().__init__()
        self.html_content = html_content
        self.page = page

    def audit_word_pertinence(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()
        # Get text and split into words, lowercasing them
        text = soup.get_text()
        words = re.findall(r'\b\w+\b', text.lower())
        # Filter out stop words
        filtered_words = [word for word in words if word not in STOP_WORDS]
        # Count the words
        count = Counter(filtered_words)
        # Select the top 5 most common words and their counts
        top_five = count.most_common(5)
        return top_five

    def run(self):
        top_five_words = self.audit_word_pertinence()
        # Extract only the words from the top five tuples and join them into a string
        top_keywords_str = ', '.join([word for word, freq in top_five_words])
        # Store the formatted string of words in the page object
        self.page.top_keywords = top_keywords_str
        print(f"Top words: {self.page.top_keywords}")

    def start_thread(self):
        th = AuditWordPertinence(html_content=self.html_content, page=self.page)
        th.start()
        return th
