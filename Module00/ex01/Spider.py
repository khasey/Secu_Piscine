import os
import sys
import requests
from bs4 import BeautifulSoup
import argparse



# Valeurs par défaut
DEFAULT_DEPTH = 5
DEFAULT_PATH = './data/'
DEFAULT_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

def Banner():
    print("""                                                                      
  / _ )
\_\(_)/_/
 _//o))_   
  /   )  
coded by KHASEY               
        """)

def main():
    Banner()
    # Configuration du parser d'options
    parser = argparse.ArgumentParser(description='Extract images from a website recursively by providing a URL as a parameter.')
    parser.add_argument('url', metavar='URL', help='URL to extract images from')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recursively download images')
    parser.add_argument('-l', '--depth-level', type=int, default=DEFAULT_DEPTH, help='Maximum depth level of the recursive download')
    parser.add_argument('-p', '--path', type=str, default=DEFAULT_PATH, help='Path where the downloaded files will be saved')
    parser.add_argument('-S', '--same-domain', action='store_true', help='Download only images from the same domain as the provided URL')
    args = parser.parse_args()

    # Creation du dossier de destination
    if not os.path.exists(args.path):
        os.makedirs(args.path)

    recursive_download(args.url, args.recursive, args.depth_level, args.path, args.same_domain)

    print('Program finished.')
    
    # Fonction récursive
def recursive_download(url, recursive, depth, path, same_domain):
    
    #condition d arret
    if depth == 0:
        return
    # Récupération du contenu de la page web
    response = requests.get(url)

    if response.status_code != 200:
        return
    
    # Parsing du HTML avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Recherche <img> dans le HTML
    for img in soup.find_all('img'):
        img_src = img.get('src')

        if img_src is None:
            continue
        # Vérification que l'URL de l'image (si l'option -S est activée)
        if same_domain and not img_src.startswith(url):
            continue

        if not any(img_src.endswith(ext) for ext in DEFAULT_EXTENSIONS):
            continue

        img_name = img_src.split('/')[-1]
        img_path = os.path.join(path, img_name)
        # Téléchargement 
        try:
            with open(img_path, 'wb') as f:
                f.write(requests.get(img_src).content)
        except Exception as e:
            print(f'Error downloading {img_src}: {e}')

    if recursive:
        for link in soup.find_all('a'):
            link_href = link.get('href')

            if link_href is None:
                continue

            if not link_href.startswith('http'):
                link_href = url + link_href
            # Appel récursif pour télécharger les images dans la page liée
            recursive_download(link_href, recursive, depth - 1, path, same_domain)

if __name__ == '__main__':
    main()
