from bs4 import BeautifulSoup
import requests
import threading


def get_html_content(url):
    response = requests.get(url)
    return response.text


def perform_analysis(url):
    html_content = get_html_content(url)
    analysis_result = analyze_html_content(html_content)
    print(analysis_result)  # Vous pouvez modifier ceci pour afficher les résultats où vous le souhaitez


def analyze_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Temps de chargement
    # (Vous pouvez utiliser des outils comme Selenium ou requests pour simuler le chargement de la page et mesurer le temps)

    # Tailles des images/vidéos
    images = soup.find_all('img')
    videos = soup.find_all('video')
    images_sizes = [len(image['src']) if image.get('src') else 0 for image in images]
    videos_sizes = [len(video['src']) if video.get('src') else 0 for video in videos]

    # Fréquences des mots dans la page
    words = soup.get_text().split()
    word_frequencies = {}
    for word in words:
        word = word.lower()
        if word.isalpha():
            if word in word_frequencies:
                word_frequencies[word] += 1
            else:
                word_frequencies[word] = 1

    # Liens entrants/sortants
    links = soup.find_all('a')
    incoming_links = [link['href'] for link in links if link.get('rel') and 'nofollow' not in link.get('rel')]
    outgoing_links = [link['href'] for link in links if link.get('rel') and 'nofollow' in link.get('rel')]

    # Alt
    images_alt = [image.get('alt') for image in images]

    # Présence de h1
    h1_presence = bool(soup.find('h1'))

    # Pertinence des mots clés
    # (Cela nécessiterait une analyse plus approfondie en utilisant une bibliothèque de traitement de langage naturel)

    # Accessibility
    # (Cela nécessiterait une analyse approfondie des balises HTML, des attributs et de l'expérience utilisateur)

    return {
        'images_sizes': images_sizes,
        'videos_sizes': videos_sizes,
        'word_frequencies': word_frequencies,
        'incoming_links': incoming_links,
        'outgoing_links': outgoing_links,
        'images_alt': images_alt,
        'h1_presence': h1_presence
    }


url = "https://fr.squarespace.com/design-de-site-web/?channel=pnb&subchannel=go&campaign=pnb-go-fr-fr-core_website-e" \
      "&subcampaign=(website-alone-fr_website_e)&gad_source=1&gclid" \
      "=CjwKCAjw17qvBhBrEiwA1rU9w2obCWL0vUETMPYkx83hHCW3ppL65QGFlF6bCuhRtxT9OscwmN8CAxoCXvwQAvD_BwE&gclsrc=aw.ds "
perform_analysis(url)
thread = threading.Thread(target=perform_analysis, args=(url,))
thread.start()
