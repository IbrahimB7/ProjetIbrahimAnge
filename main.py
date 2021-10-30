#!/bin/env python3 

from bs4 import BeautifulSoup
from Projet import Ressource
from Projet import Collecte
from Projet import Traitement
from Projet import Prisme

u1 = "http://math.univ-angers.fr"
u2 = "https://math.univ-angers.fr/documents/exercices_terminale_septembre_2014.pdf"


U = [u1,u2]
un_prisme = Prisme(Traitement)
un_prisme.run(U)
un_prisme.show()
