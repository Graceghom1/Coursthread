from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from ref.Calculator import Calculator
from ref.page import Page




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
            page_links = soup.find_all('a', href=True)

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







start_url = 'https://wordcount.com/'

page = Page(url=start_url)
page.initPage()

# Appeler la fonction pour obtenir les liens uniques
#unique_links = get_unique_links(start_url)

# # Afficher les liens uniques
# print("Liens uniques trouvés sur la page principale et les pages liées :")
# for link in unique_links:
#     print(link)


pages = []

nextPages = page.links

for link in nextPages:
    p = Page(url=link)
    # p.initPage()
    pages.append(p)




print("pppppppp")