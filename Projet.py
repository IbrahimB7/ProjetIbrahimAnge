#!/bin/env python3 

import requests
import os
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader 


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
            self.texte = soup.get_text() #Extrait le texte de la page
        
        elif self.objet == 'PDF':    
            path = os.getcwd() #obtient le chemin du fichier
            file_path = os.path.join(path,os.path.basename(self.url))  #Fichier ou l'on va telecharge le pdf tout en conservant son nom
            self.nom = os.path.basename(self.url) #on conserve le nom du PDF telechargé
            with open(file_path, 'wb') as f:  #telecharge le fichier pdf
                f.write(self.request.content)
            with open(file_path,'rb'):
                pdf =  PdfFileReader(os.path.basename(self.url)) #ouvre le pdf
                npage = pdf.getNumPages()
                self.texte=''
                for i in range(npage):
                    page = pdf.getPage(i)
                    self.texte += page.extractText() 
                    
            
                
class Collecte(Ressource):  
    def __init__(self, urls):
        self.urls = urls
        self.ressources = []

    def run(self): #Crée une liste des ressources 
        for url in self.urls:
            texte = Ressource(url)
            texte.text()
            self.ressources.append(texte)
    
    def content(self):  #Crée une liste une liste des textes, une par ressource  
        self.textes = []
        for i in self.ressources:
            self.textes.append(i.texte)
        return self.textes
    

class Traitement(Collecte):
    def __init__(self):
        self.Traitement=[]

    def load(self,u):
        self.Traitement += u

    def run(self):
        self.nombre = []
        for i in self.Traitement:
            mots = i.split()
            nombre = len(mots)
            self.nombre.append(nombre)
    
    def show(self):
        print(self.nombre)

class Prisme(Traitement):
    def __init__(self,Traitement):
        self.T = Traitement

    def run(self,Fichier):
        self.u = Collecte(Fichier)
        self.u.run()
        self.u.content()
        self.Tr = Traitement()
        self.Tr.load(self.u.textes)
        self.Tr.run()
    
    def show(self):
        self.Tr.show()


    
    
        
