#!/bin/env python3 

import requests
from bs4 import BeautifulSoup
from io import BytesIO
from pdfminer.high_level import extract_text
from requests_html import HTMLSession
from urllib.parse import urljoin
import pathlib,webbrowser
from wordcloud import WordCloud


class Ressource():
    def __init__(self,url):
        self.url = url
        self.request = requests.get(self.url)
        self.contenu = self.request.headers.get('content-type')
        if 'pdf' in self.contenu:
            self.objet = 'PDF'
        elif 'html' in self.contenu:
            self.objet = 'HTML'    

    def type(self):
        print(self.objet)

    def text(self):
        if self.objet == 'HTML':
            soup = BeautifulSoup(self.request.text,'html.parser')
            for s in soup.select('script'):
                s.extract()
            for s in soup.select('style'):
                s.extract()            
            self.texte = soup.get_text() #Extrait le texte de la page
        
        elif self.objet == 'PDF':    #Pris du programme de Tasli-Legruel 
            pdf = BytesIO(self.request.content)
            self.texte=extract_text(pdf)
            return self.texte

    def image(self):
    
        if self.objet == "HTML" :
    
            self.imgurls = []
            session = HTMLSession()
            r = session.get(self.url)            
            r.html.render(timeout=20)            
            soup = BeautifulSoup(r.html.html, "html.parser")            
            for img in soup.find_all("img"):
                url = img.attrs.get("src") or img.attrs.get("data-src") or img.attrs.get("data-original")
                
                if not url:
                    continue

                url = urljoin(self.url, url)

                try:
                    pos = url.index("?")
                    url = url[:pos]
                except ValueError:
                    pass

                self.imgurls.append(url)

            session.close()
            return self.imgurls
                
class Collecte():  
    def __init__(self, urls):
        self.urls = urls
        self.ressources = []

    def run(self): #Crée une liste des ressources 
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
            image = Ressource(url)
            image.image()
            self.images.append(image)       
        for i in self.images:
            self.ressources.append(i.imgurls)



    def content(self): 
        return self.ressources
    

class Traitement():
    def load(self,fichiers):
        self.fichiers = fichiers

    def run(self): # run texte
        self.wordcloud = []        
        pathlib.Path('WordCloud').mkdir(parents=False, exist_ok=True) 
        k=0
        for i in self.fichiers:            
            wordcloud = WordCloud(background_color='white',max_font_size=50).generate(i)            
            save_dir = f"WordCloud/{k}.png"            
            wordcloud.to_file(save_dir)
            self.wordcloud.append(save_dir)
            k+=1
    
    def show(self):
        base = """
                <html>
                    <head>
        
                    </head>
                </html> 
                """        
        soup = BeautifulSoup(base, features="html.parser")        
        for i in self.wordcloud:
            new_image = soup.new_tag("img", src=i, style="display:block")
            soup.head.append(new_image)        
            soup.head.append(soup.new_tag('br'))
        with open("result.html", "w") as f:
            f.truncate(0)
            f.write(str(soup))        
        webbrowser.open('result.html')

class Prisme():
    def __init__(self,traitement):
        self.traitement = traitement

    def run(self,Fichier):
        if self.traitement=='Nuage':
            file = open(Fichier,'r')
            url = [i.strip() for i in file.readlines()]
            collecte = Collecte(url)
            collecte.run()
            Tr = Traitement()
            Tr.load(collecte.content())
            Tr.run()
            self.Tr = Tr

        elif self.traitement=='Image':
            pass
    
    def show(self):
        if self.traitement=='Nuage':
            self.Tr.show()
        elif self.traitement=='Image':
            pass


    
    
        