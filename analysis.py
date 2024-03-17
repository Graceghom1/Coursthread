# analysis.py
import requests
from bs4 import BeautifulSoup
import time
from collections import Counter


def get_html_content(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        return response.text, end_time - start_time, None  # No error occurred
    except Exception as e:
        return "", 0, str(e)  # Return empty content, zero time, and the error message

def calculate_word_frequencies(text):
    try:
        words = text.lower().split()
        clean_words = [word for word in words if word.isalpha()]
        word_frequencies = Counter(clean_words)
        return dict(word_frequencies.most_common(10)), None  # Return word frequencies and no error
    except Exception as e:
        return {}, f"Error calculating word frequencies: {e}"  # Return error message


def analyze_html_content(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Count images and videos
        images = soup.find_all('img')
        videos = soup.find_all('video')
        image_count = len(images)
        video_count = len(videos)

        # Calculate word frequencies
        text = soup.get_text().lower()
        words = [word for word in text.split() if word.isalpha()]
        word_frequencies = Counter(words)

        # Categorize links as incoming or outgoing
        links = soup.find_all('a')
        incoming_links = [link['href'] for link in links if 'http' not in link.get('href', '')]
        outgoing_links = [link['href'] for link in links if 'http' in link.get('href', '')]

        # Check for the presence of H1 tags
        h1_presence = 'Yes' if soup.find('h1') else 'No'

        # Assemble all analysis results into a structured dictionary
        analysis_results = {
            "Loading Time": None,  # Placeholder for loading time
            "Word Frequency": word_frequencies.most_common(10),  # Directly use Counter object
            "Copy Paste Enabled": None,  # Placeholder for copy paste enabled
            "Outbound/Inbound Links": (len(incoming_links), len(outgoing_links)),  # Use lengths directly
            "Image Sizes": (image_count, video_count),  # Directly use counts
            "Number of H1 in Source Code": h1_presence,
            "Keywords Pertinence": None,  # Placeholder for keyword pertinence
            "Is the Website Mobile Friendly": None,  # Placeholder for mobile friendly
            "Is the Website Accessible": None  # Placeholder for accessibility
        }

        return analysis_results, None  # Return results as a dictionary and no error

    except Exception as e:
        # If an error occurred, return an empty dictionary and the error message
        return {}, f"Error analyzing HTML content: {e}"
