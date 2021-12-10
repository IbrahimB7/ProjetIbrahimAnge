#!/bin/env python3 

import os
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from pdfminer.high_level import extract_text
from requests_html import HTMLSession
from urllib.parse import urljoin
import pathlib,webbrowser
from wordcloud import WordCloud
import fitz
import io
from PIL import Image
from maconfig import *

'''Lire le fichier requirements.txt pour voir les modules à installer!'''



#------------------
'''RESSOURCE'''
#------------------

class Ressource():
    def __init__(self,url):
        self.url = url
        self.request = requests.get(self.url)
        self.contenu = self.request.headers.get('content-type')
        if 'pdf' in self.contenu: #recupere le type de fichier HTML ou PDF
            self.objet = 'PDF'
        elif 'html' in self.contenu:
            self.objet = 'HTML'    

    def type(self):
        print(self.objet)

    def text(self):
        pathlib.Path('WordCloud').mkdir(parents=False, exist_ok=True) #Création du fichier image, ou l'on va stocker les nuages de mots
        if self.objet == 'HTML': #Pris du programme de Tasli-Legruel 
            soup = BeautifulSoup(self.request.text,'html.parser')
            for s in soup.select('script'):
                s.extract()
            for s in soup.select('style'):
                s.extract()            
            self.texte = soup.get_text() 
        
        elif self.objet == 'PDF':    #Pris du programme de Tasli-Legruel 
            pdf = BytesIO(self.request.content)
            self.texte=extract_text(pdf)
            return self.texte

    def image(self):
        pathlib.Path('image').mkdir(parents=False, exist_ok=True) #Création du fichier image, ou l'on va stocker les images (d'un PDF ou HTML)

        if self.objet == "HTML" :
            '''On récupère seulement les urls des images de la page qu'on a request'''
            self.imgurls = []
            pathlib.Path('image/HTML').mkdir(parents=False, exist_ok=True) #Création du fichier ou l'on va stocker les images d'un HTML
            session = HTMLSession()
            r = session.get(self.url)            
            soup = BeautifulSoup(r.html.html, "html.parser")           
            for img in soup.find_all("img"):
                url = img.attrs.get("src") or img.attrs.get("data-src") or img.attrs.get("data-original")               
                
                url = urljoin(self.url, url)             
                self.imgurls.append(url)

            session.close()
            return self.imgurls #renvoi liste d'url des images
        
        if self.objet == "PDF":

            '''Pour récupérer les images, il faut d'abord que l'on télécharge le fichier PDF dans le fichier actuel, 
            contrairement à l'html on ne peut pas extraire les liens des images d'un PDF comme on le ferait avec une page HTML'''
            self.imgurls = ['PDF']
            pathlib.Path('image/PDF').mkdir(parents=False, exist_ok=True) #Fichier ou on va stocker les images du PDF
            path = os.getcwd() #obtient le chemin du fichier
            file_path = os.path.join(path,os.path.basename(self.url))  #Fichier ou l'on va telecharge le pdf tout en conservant son nom
            self.nom = os.path.basename(self.url) #on conserve le nom du PDF telechargé
            with open(file_path, 'wb') as f:  #telecharge le fichier pdf
                f.write(self.request.content)
            doc = fitz.open(self.nom)
            for pages in range(len(doc)):  #On récupère toutes les images dans le dossier image/PDF
                page = doc[pages]
                for imageindex, img in enumerate(page.getImageList(),start = 1):
                    xref = img[0]
                    baseimage = doc.extractImage(xref)
                    ib = baseimage["image"]
                    ie = baseimage["ext"]
                    image = Image.open(io.BytesIO(ib))
                    image.save(open(f"image/PDF/image{pages+1}_{imageindex}.png", "wb"))
            return self.imgurls  #Renvoie ['PDF'] qui sera utile pour le traitement des images du PDF par la suite
                
#------------------
'''COLLECTE'''
#------------------       
                
class Collecte():  
    def __init__(self, urls):
        self.urls = urls
        self.ressources = []

    def run(self):
        self.textes = []
        for url in self.urls:
            texte = Ressource(url)
            texte.text()
            self.textes.append(texte)
        for i in self.textes:
            self.ressources.append(i.texte)

    def runimg(self):
        self.images = []
        for url in self.urls:
            imge = Ressource(url)        
            imge.image()
            self.images.append(imge)       
        for i in self.images:
            self.ressources.append(i.imgurls)
        

    def content(self): 
        return self.ressources

#------------------
'''TRAITEMENT'''
#------------------

class Traitement():
    def load(self,fichiers): 
        self.fichiers = fichiers

    def run(self): #Utilisation du module wordcloud pour créer le nuage de mots
        self.wordcloud = []        
        k=0 
        for i in self.fichiers:   #crée un nuage par texte         
            wordcloud = WordCloud(background_color=couleur_fond,stopwords = mots_exclus, max_words=nombre_mots,max_font_size=font_size).generate(i)   #Paramètre variables, à modifier dans maconfig.py     
            save_dir = f"WordCloud/{k}.png"     #enregistre un nuage dans le nuage        
            wordcloud.to_file(save_dir)
            self.wordcloud.append(save_dir) #on ajoute le chemin du fichier image du nuage a la liste pour le show 
            k+=1
    
    def show(self):
        base = """ 
                <html>
                    <head>
        
                    </head>
                </html> 
                """        #la base du code de la page html ou l'on va afficher nos images
        soup = BeautifulSoup(base, features="html.parser")        
        for i in self.wordcloud: #On ajoute dans le code tous les nuages de mots que l'on a obtenu au préalable
            new_image = soup.new_tag("img", src=i, style="display:block")
            soup.head.append(new_image)        
            soup.head.append(soup.new_tag('br'))
        with open("nuages.html", "w") as f:
            f.truncate(0)
            f.write(str(soup))        
        webbrowser.open('nuages.html')     #ouvre une page nuages.html avec tous les nuages de points dessus

    def runimg(self):
        self.images=[]
        k=0
        for url in self.fichiers:
            if url == ['PDF']:  ## si c'est un fichier PDF
                for filename in os.listdir(f'{os.getcwd()}/image/PDF'): #on ajoute a la liste self.images le chemin et nom des images enregistré dans image/PDF
                    self.images.append(f'{os.getcwd()}/image/PDF/{filename}')


            else:   ##fichier HTML On télécharge les images dans le fichier image/HTML
                for i in url:
                    file_ext = i.split('.')[-1]
                    with open(f'image/HTML/{k}.{file_ext}', 'wb') as f:
                        f.write(requests.get(i).content)

                    self.images.append(f"image/HTML/{k}.{file_ext}") #on ajoute a la liste self.images le chemin et nom des différentes images
                    k+=1
                

    def showimg(self):
        base = """
                <html>
                    <head>
        
                    </head>
                </html> 
                """ #la base du code de la page html ou l'on va afficher nos images
        
        soup = BeautifulSoup(base, features="html.parser")

        for i in self.images: #On ajoute dans le code html toutes les images, a partir des chemins récuperer dans le runimg juste au dessus
            new_image = soup.new_tag("image", src=i, style="display:block")
            soup.head.append(new_image)        
            soup.head.append(soup.new_tag('br'))

        with open("allimgs.html", "w") as f: #on formate notre page de resultat
            f.truncate(0)
            f.write(str(soup))
        
        webbrowser.get(navigateurpath).open('allimgs.html')

#------------------
'''PRISME'''
#------------------
class Prisme():
    def __init__(self,traitement):
        self.traitement = traitement

    def run(self,urls):        
        collecte = Collecte(urls)
        if self.traitement=='Nuage':
            collecte.run()
        elif self.traitement=='Image':
            collecte.runimg()
        self.Tr = Traitement()
        self.Tr.load(collecte.content())
        if self.traitement=='Nuage':
            self.Tr.run()
        elif self.traitement=='Image':
            self.Tr.runimg()
        
        
    def show(self):
        if self.traitement=='Nuage':
            self.Tr.show()
        elif self.traitement=='Image':
            return self.Tr.showimg()


    
    
        
