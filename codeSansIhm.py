import requests
from bs4 import BeautifulSoup
import threading
import base64
import urllib.parse

# Fonction pour récupérer le contenu HTML d'une URL
def get_html_content(url):
    response = requests.get(url)
    return response.content

# Fonction pour extraire les balises <img> et <video> d'une page web
def extract_media_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    video_tags = soup.find_all('video')
    return img_tags, video_tags

# Fonction pour obtenir la taille d'une image à partir de son URL ou de son contenu base64
def get_image_size(image_src):
    if image_src.startswith('data:image'):
        # Si l'URL commence par 'data:image', c'est une image encodée en base64
        return get_base64_image_size(image_src.split(',')[1])  # Sépare les métadonnées et récupère les données base64
    else:
        try:
            with urllib.request.urlopen(image_src) as response:
                return response.length
        except Exception as e:
            print(f"Erreur lors de la récupération de la taille de l'image {image_src}: {e}")
            return None

# Fonction pour obtenir la taille d'une image encodée en base64
def get_base64_image_size(base64_data):
    try:
        image_data = base64.b64decode(base64_data)
        image_size = len(image_data)
        return image_size
    except Exception as e:
        print(f"Erreur lors de la récupération de la taille de l'image encodée en base64: {e}")
        return None

# Fonction pour obtenir la taille d'une vidéo à partir de son URL
def get_video_size(video_url):
    try:
        with urllib.request.urlopen(video_url) as response:
            return response.length
    except Exception as e:
        print(f"Erreur lors de la récupération de la taille de la vidéo {video_url}: {e}")
        return None

# Fonction pour auditer les tailles des médias
def audit_media_sizes(media_tags, media_type):
    for media_tag in media_tags:
        media_src = media_tag.get('src')
        media_size = get_image_size(media_src) if media_type == 'image' else get_video_size(media_src)
        if media_size:
            print(f"{media_type.capitalize()}: {media_src}, Taille: {media_size} octets")

# Fonction pour auditer la présence des balises <h1>
def audit_h1_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    h1_tags = soup.find_all('h1')
    if h1_tags:
        print("Les balises <h1> sont présentes sur la page.")
    else:
        print("Attention : Aucune balise <h1> n'a été trouvée sur la page.")

# Fonction pour auditer la présence des mots-clés
def audit_keywords(html_content, mots_cles):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text().lower()
    for mot_cle in mots_cles:
        if mot_cle.lower() in text:
            print(f"Le mot-clé '{mot_cle}' est présent sur la page.")
        else:
            print(f"Attention : Le mot-clé '{mot_cle}' n'a pas été trouvé sur la page.")

# Fonction pour exécuter l'audit d'une page
def audit_page(url):
    html_content = get_html_content(url)
    audit_h1_tags(html_content)
    img_tags, video_tags = extract_media_tags(html_content)
    audit_media_sizes(img_tags, 'image')
    audit_media_sizes(video_tags, 'video')

    audit_keywords(html_content, ['mot_cle_1', 'mot_cle_2', 'mot_cle_3'])
    # Parcourir en profondeur les liens sur la page
    links = extract_links(html_content, url)
    for link in links:
        thread = threading.Thread(target=audit_page, args=(link,))
        thread.start()



        def get_unique_links(url):
            # Ensembles pour stocker les liens uniques et les liens déjà visités
            unique_links = set()
            visited_links = set()
            links_to_visit = set([url])

            # Parcourir tous les liens à visiter
            while links_to_visit:
                # Récupérer un lien à visiter
                current_url = links_to_visit.pop()

                # Vérifier si le lien a déjà été visité pour éviter les boucles infinies
                if current_url in visited_links:
                    continue

                # Ajouter le lien aux liens visités
                visited_links.add(current_url)

                # Envoyer une requête HTTP GET à l'URL
                response = requests.get(current_url)

                # Vérifier si la requête a réussi
                if response.status_code == 200:
                    # Analyser le contenu HTML de la réponse
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Trouver tous les liens dans la page
                    page_links = soup.find_all('a')

                    # Parcourir tous les liens de la page actuelle
                    for link in page_links:
                        href = link.get('href')

                        # Vérifier si le lien est valide et non vide
                        if href and href.startswith('http'):
                            absolute_url = urljoin(current_url, href)
                            unique_links.add(absolute_url)
                            # Ajouter le lien à la liste des liens à visiter si ce n'est pas déjà visité
                            if absolute_url not in visited_links:
                                links_to_visit.add(absolute_url)

            return unique_links

        # Appeler la fonction pour obtenir les liens uniques
        unique_links = get_unique_links(url)

        # Afficher les liens uniques
        print("Liens uniques trouvés sur la page principale et les pages liées :")
        for link in unique_links:
            print(link)


# Fonction pour extraire les liens à partir du contenu HTML d'une page
def extract_links(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=True)
    absolute_links = []
    for link in links:
        absolute_link = urllib.parse.urljoin(base_url, link['href'])
        absolute_links.append(absolute_link)
    return absolute_links

# URL de départ pour l'audit
# start_url = 'https://blog.hubspot.fr/marketing'
start_url = 'https://www.cleor.com/'

# Audit de la page de départ
audit_page(start_url)
