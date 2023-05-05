#!/usr/bin/env python
# coding: utf-8

# # Phase 1

# Choisissez n'importe quelle page Produit sur le site de Books to Scrape. Écrivez un
# script Python qui visite cette page et en extrait les informations suivantes :
# 
# - product_page_url
# - universal_ product_code (upc)
# - title
# - price_including_tax
# - price_excluding_tax
# - number_available
# - product_description
# - category
# - review_rating
# - image_url
# 
# Écrivez les données dans un fichier CSV qui utilise les champs ci-dessus comme
# en-têtes de colonnes.
# 

# In[1]:


pip install beautifulsoup4


# In[2]:


import requests
from bs4 import BeautifulSoup
import csv

# Envoyer une requête HTTP à la page produit
response = requests.get('http://books.toscrape.com/catalogue/the-black-maria_991/index.html')

# Parser le contenu HTML de la page produit avec BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Extraire les informations requises de la page produit
product_page_url = 'http://books.toscrape.com/catalogue/the-black-maria_991/index.html'
universal_product_code = soup.find('th', string='UPC').find_next_sibling('td').text
title = soup.find('h1').text
price_including_tax = soup.find('th', string='Price (incl. tax)').find_next_sibling('td').text
price_excluding_tax = soup.find('th', string='Price (excl. tax)').find_next_sibling('td').text
number_available = soup.find('th', string='Availability').find_next_sibling('td').text.strip()
product_description = soup.find('div', {'id': 'product_description'}).find_next_sibling('p').text.strip()
category = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2].text
review_rating = soup.find('p', {'class': 'star-rating'}).get('class')[1]
image_url = soup.find('div', {'class': 'item active'}).find('img')['src']



# In[3]:


# Écrire les données dans un fichier CSV
import csv

with open('product_info.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 
                     'price_excluding_tax', 'number_available', 'product_description', 'category',
                     'review_rating', 'image_url'])
    writer.writerow([product_page_url, universal_product_code, title, price_including_tax, 
                     price_excluding_tax, number_available, product_description, category,
                     review_rating, image_url])


# # Phase 2
# 

# Maintenant que vous avez obtenu les informations concernant un premier livre,
# vous pouvez essayer de récupérer toutes les données nécessaires pour toute une
# catégorie d'ouvrages.
# 
# Choisissez n'importe quelle catégorie sur le site de Books to Scrape. Écrivez un
# script Python qui consulte la page de la catégorie choisie, et extrait l'URL de la
# page Produit de chaque livre appartenant à cette catégorie.
# 
# Combinez cela avec le travail que vous avez déjà effectué dans la phase 1 afin
# d'extraire les données produit de tous les livres de la catégorie choisie, puis écrivez
# les données dans un seul fichier CSV.
# 
# Remarque : certaines pages de catégorie comptent plus de 20 livres, qui sont
# donc répartis sur différentes pages (« pagination »). Votre application doit être
# capable de parcourir automatiquement les multiples pages si présentes.
# 

# In[4]:


import requests
from bs4 import BeautifulSoup
import csv

# Définir l'URL de la page de la catégorie choisie
category_url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'

# Envoyer une requête GET à l'URL de la catégorie et récupérer le contenu HTML de la réponse
response = requests.get(category_url)
html = response.content

# Parser le contenu HTML avec Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Trouver tous les liens de page produit dans la page de catégorie
product_links = soup.select('.product_pod h3 a')

# Créer une liste pour stocker les données de chaque livre
books_data = []

# Parcourir les liens de page produit et extraire les informations nécessaires pour chaque livre
for link in product_links:
    # Construire l'URL de la page produit à partir du lien relatif trouvé
    product_url = 'http://books.toscrape.com/catalogue/' + link['href'].replace('../', '')
    
    # Envoyer une requête GET à l'URL de la page produit et récupérer le contenu HTML de la réponse
    response = requests.get(product_url)
    html = response.content
    
    # Parser le contenu HTML avec Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extraire les informations nécessaires de la page produit
    product_page_url = product_url
    title = soup.select_one('.product_main h1').text
    td_element = soup.select_one('table tr:nth-of-type(1) td')
    universal_product_code = td_element.text if td_element else None
    td_element = soup.select_one('table tr:nth-of-type(2) td')
    price_excluding_tax = td_element.text if td_element else None
    td_element = soup.select_one('table tr:nth-of-type(3) td')
    price_including_tax = td_element.text if td_element else None
    td_element = soup.select_one('table tr:nth-of-type(5) td')
    number_available = td_element.text if td_element else None
    product_description = soup.select_one('#product_description + p').text
    category = soup.select('.breadcrumb li')[2].text.strip()
    td_element = soup.select_one('p.star-rating')
    review_rating = td_element['class'][1] if td_element else None
    img_element = soup.select_one('.item img')
    image_url = 'http://books.toscrape.com/' + img_element['src'].replace('../', '')
    
    # Ajouter les informations du livre dans la liste
    book_data = [product_page_url, universal_product_code, title, price_including_tax, 
                 price_excluding_tax, number_available, product_description, category,
                 review_rating, image_url]
    books_data.append(book_data)

# Écrire les données de tous les livres dans un fichier CSV
with open('mystery_books.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 
                     'price_excluding_tax', 'number_available', 'product_description', 'category',
                     'review_rating', 'image_url'])
    writer.writerows(books_data)


# # Phase 3

# Ensuite, étendez votre travail à l'écriture d'un script qui consulte le site de Books to Scrape, extrait toutes les catégories de livres disponibles, puis extrait les informations produit de tous les livres appartenant à toutes les différentes catégories. 
# 
# Vous devrez écrire les données dans un fichier CSV distinct pour chaque catégorie de livres.
# 

# In[5]:


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

base_url = 'http://books.toscrape.com/'

# Fonction pour extraire les données d'un livre
def get_book_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    try:
        title = soup.select_one('h1').text
    except:
        title = 'N/A'
        
    try:
        price_including_tax = soup.select_one('.price_color').text
    except:
        price_including_tax = 'N/A'
        
    try:
        price_excluding_tax = soup.select_one('table tr:nth-of-type(3) td').text
    except:
        price_excluding_tax = 'N/A'
        
    try:
        number_available = soup.select_one('table tr:nth-of-type(6) td').text.strip()
    except:
        number_available = 'N/A'
        
    try:
        product_description = soup.select_one('#product_description ~ p').text
    except:
        product_description = 'N/A'
        
    try:
        category = soup.select('.breadcrumb li:nth-of-type(3) a')[0].text.strip()
    except:
        category = 'N/A'
        
    try:
        review_rating_tag = soup.select_one('.product_page_rating p')['class'][1]
        review_rating = review_rating_tag.replace('star-rating', '').strip()
    except:
        review_rating = 'N/A'
    
    book_data = {
        'Title': title,
        'Price (incl. tax)': price_including_tax,
        'Price (excl. tax)': price_excluding_tax,
        'Availability': number_available,
        'Product Description': product_description,
        'Category': category,
        'Review Rating': review_rating
    }
    
    return book_data

# Récupération des liens de toutes les catégories
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')
categories_links = soup.select('.side_categories a')
categories_urls = [urljoin(base_url, link['href']) for link in categories_links]

# Extraction des données de chaque livre pour chaque catégorie et écriture dans un fichier CSV distinct
for category_url in categories_urls:
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    category_name = soup.select('.page-header h1')[0].text.strip()
    books_urls = [urljoin(category_url, link['href']) for link in soup.select('.product_pod h3 a')]
    
    with open(f'{category_name}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Price (incl. tax)', 'Price (excl. tax)', 'Availability', 'Product Description', 'Category', 'Review Rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for book_url in books_urls:
            book_data = get_book_data(book_url)
            writer.writerow(book_data)


# Ce code va créer un fichier CSV distinct pour chaque catégorie de livres sur le site "Books to Scrape" et écrire les données de tous les livres appartenant à chaque catégorie dans leur propre fichier CSV.

# # Phase 4

# Enfin, prolongez votre travail existant pour télécharger et enregistrer le fichier image de chaque page Produit que vous consultez.

# In[6]:


import csv
import requests
import shutil
from bs4 import BeautifulSoup

# Liste des catégories
categories_urls = [
    'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html',
    'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'
]

# Fonction pour récupérer les informations d'une page produit
def get_product_information(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_page_url = product_url
    upc = soup.find('th', text='UPC').find_next_sibling('td').text
    title = soup.find('h1').text.strip()
    price_including_tax = soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text
    price_excluding_tax = soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text
    number_available = soup.find('th', text='Availability').find_next_sibling('td').text
    product_description = soup.find('div', {'id': 'product_description'}).find_next_sibling('p').text
    category = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2].text.strip()
    review_rating = soup.find('p', {'class': 'star-rating'})['class'][1]
    image_url = soup.find('img')['src'].replace('../..', 'http://books.toscrape.com')
    return [product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url]

# Fonction pour récupérer toutes les URLs des pages produits d'une catégorie
def get_category_product_urls(category_url):
    product_urls = []
    page_url = category_url
    while True:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_links = soup.find_all('a', {'class': 'booktitle'})
        for link in product_links:
            product_url = link['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
            product_urls.append(product_url)
        next_button = soup.find('li', {'class': 'next'})
        if next_button is None:
            break
        else:
            page_url = category_url.replace('index.html', next_button.find('a')['href'])
    return product_urls

# Fonction pour enregistrer l'image d'une page produit
def download_product_image(image_url, filepath):
    response = requests.get(image_url, stream=True)
    with open(filepath, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

# Parcours de toutes les catégories
for category_url in categories_urls:
    # Récupération des URLs des pages produits de la catégorie
    product_urls = get_category_product_urls(category_url)

    # Récupération des informations de chaque page produit
    products_data = []
    for product_url in product_urls:
        product_data = get_product_information(product_url)
        products_data.append(product_data)

        # Téléchargement de l'image de la page produit
        image_url = product_data[-1]
        image_filename = image_url.split('/')[-1]
        image_filepath = f'{category_url.split("/")[-2]}_images/{image_filename}'
        download_product_image(image_url, image_filepath)

    


# In[7]:


# Enregistrement des données dans un fichier CSV
import csv

# Les données à enregistrer dans le fichier CSV
data = [
    ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax",
     "number_available", "product_description", "category", "review_rating", "image_url"],
    ["http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html", "a897fe39b1053632",
     "A Light in the Attic", "£51.77", "£45.17", "1000", "It's hard to imagine a world without A Light in the Attic.",
     "Poetry", "Three", "http://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg"],
    ["http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html", "90fa61229261140a",
     "Tipping the Velvet", "£53.74", "£44.10", "20", "Erotic and absorbing, this is a truly remarkable debut novel.",
     "Historical Fiction", "One", "http://books.toscrape.com/media/cache/da/54/da549f5cd5f74342c1b7e3f1ab8b1f1e.jpg"]
]

# Enregistrement des données dans le fichier CSV
with open("booksFinal.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)


# In[8]:


import csv
import requests
import shutil
from bs4 import BeautifulSoup
import os

# Liste des catégories
categories_urls = [    'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html',    'http://books.toscrape.com/catalogue/category/books/travel_2/index.html']

# Fonction pour récupérer les informations d'une page produit
def get_product_information(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_page_url = product_url
    upc = soup.find('th', text='UPC').find_next_sibling('td').text
    title = soup.find('h1').text.strip()
    price_including_tax = soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text
    price_excluding_tax = soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text
    number_available = soup.find('th', text='Availability').find_next_sibling('td').text
    product_description = soup.find('div', {'id': 'product_description'}).find_next_sibling('p').text
    category = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2].text.strip()
    review_rating = soup.find('p', {'class': 'star-rating'})['class'][1]
    image_url = soup.find('img')['src'].replace('../..', 'http://books.toscrape.com')
    return [product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url]

# Fonction pour récupérer toutes les URLs des pages produits d'une catégorie
def get_category_product_urls(category_url):
    product_urls = []
    page_url = category_url
    while True:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_links = soup.find_all('a', {'class': 'booktitle'})
        for link in product_links:
            product_url = link['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
            product_urls.append(product_url)
        next_button = soup.find('li', {'class': 'next'})
        if next_button is None:
            break
        else:
            page_url = category_url.replace('index.html', next_button.find('a')['href'])
    return product_urls

# Fonction pour enregistrer l'image d'une page produit
def download_product_image(image_url, filepath):
    response = requests.get(image_url, stream=True)
    with open(filepath, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

# Parcours de toutes les catégories
for category_url in categories_urls:
    # Création du dossier pour enregistrer les images
    category_folder = category_url.split('/')[-2] + '_images'
    os.makedirs(category_folder, exist_ok=True)

    # Récupération des URLs des pages produits de la catégorie
    product_urls = get_category_product_urls(category_url)

    # Récupération des informations de chaque page produit
    products_data


# In[9]:


import requests
import os
from bs4 import BeautifulSoup
import urllib

# Fonction pour télécharger et enregistrer une image
def save_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)

# URL de la page d'accueil du site à scraper
url = 'http://books.toscrape.com/'

# Récupération du contenu HTML de la page d'accueil
response = requests.get(url)

if response.status_code == 200:

    # Création d'un objet BeautifulSoup à partir du contenu HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Récupération de tous les liens de catégorie
    category_links = soup.select('div.side_categories > ul > li > ul > li > a')

    # Boucle sur chaque lien de catégorie
    for category_link in category_links:

        # Récupération de l'URL de la catégorie
        category_url = urllib.parse.urljoin(url, category_link['href'])

        # Récupération du contenu HTML de la page de la catégorie
        response = requests.get(category_url)

        if response.status_code == 200:

            # Création d'un objet BeautifulSoup à partir du contenu HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Récupération de tous les liens de livre sur la page
            book_links = soup.select('h3 > a')

            # Boucle sur chaque lien de livre
            for book_link in book_links:

                # Récupération de l'URL de la page de produit
                book_url = urllib.parse.urljoin(category_url, book_link['href'])

                # Récupération du contenu HTML de la page de produit
                response = requests.get(book_url)

                if response.status_code == 200:

                    # Création d'un objet BeautifulSoup à partir du contenu HTML
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Récupération de l'URL de l'image du livre
                    image_url = urllib.parse.urljoin(book_url, soup.select_one('div.item > img')['src'])

                    # Récupération du nom du fichier à partir de l'URL de l'image
                    filename = os.path.basename(image_url)

                    # Téléchargement et enregistrement de l'image
                    save_image(image_url, filename)


# extrat

# In[ ]:


import requests
import csv
import os
from bs4 import BeautifulSoup


# Création d'un dossier pour les images
if not os.path.exists("images"):
    os.makedirs("images")

# URL de la page principale
base_url = "http://books.toscrape.com/index.html"

# Récupération du contenu de la page principale
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

# Récupération de tous les liens des catégories de livres
category_links = []
sidebar = soup.find("div", {"class": "side_categories"})
categories = sidebar.find_all("a")
for category in categories:
    category_links.append("http://books.toscrape.com/" + category["href"])

# Récupération de tous les liens des pages de livres de chaque catégorie
book_links = []
for category_link in category_links:
    response = requests.get(category_link)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("h3")
    for book in books:
        book_link = book.find("a")["href"]
        book_links.append("http://books.toscrape.com/catalogue/" + book_link)

# Récupération des informations de chaque page produit
products_data = []
for book_link in book_links:
    response = requests.get(book_link)
    soup = BeautifulSoup(response.text, "html.parser")

    # Récupération du titre
    title = soup.find("h1").text

    # Récupération de la catégorie
    category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")[2].text.strip()

    # Récupération des informations du produit
    table = soup.find("table", {"class": "table-striped"})
    rows = table.find_all("tr")
    upc = rows[0].find_all("td")[0].text.strip()
    price_including_tax = rows[3].find_all("td")[1].text.strip()
    price_excluding_tax = rows[2].find_all("td")[1].text.strip()
    number_available = rows[5].find_all("td")[1].text.strip()
    review_rating = rows[6].find_all("td")[1].text.strip()

    # Récupération de la description du produit
    product_description = soup.find_all("p")[3].text.strip()

    # Récupération de l'URL de l'image
    image_url = "http://books.toscrape.com/" + soup.find("img")["src"][6:]

    # Enregistrement de l'image
    image_response = requests.get(image_url)
    with open("images/" + upc + ".jpg", "wb") as f:
        f.write(image_response.content)

    # Ajout des informations du produit à la liste des données de produits
    product_data = [book_link, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url]
    products_data.append(product_data)

# Enregistrement des données dans le fichier CSV
with open("booksFinal.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(products_data)


# In[ ]:




