#!/bin/env python3 

'''Lire le fichier requirements.txt pour voir les modules à installer!'''


urls = ['https://math.univ-angers.fr/','https://math.univ-angers.fr/documents/exercices_terminale_septembre_2014.pdf']  #Liste de liens 
'''Après avoir changer les urls au dessus, il peut que la page html allimgs.html ne s'actualisent pas. Si ce n'est pas le cas, il faut actualiser manuellement la page '''

navigateurpath = None  #Navigateur par défaut choisi, remplacer None par 'PATH' avec PATH le chemin du navigateur à choisir (Ne semble pas fonctionner sur windows?)


#Paramètres nuage de mots
mots_exclus = ['de']  #Ecrire les mots à exclure entre ''  
nombre_mots = 100 #Choisir le nombre de mot à avoir dans le nuage de mot
couleur_fond = 'white' #Choisir la couleur du fond 
font_size = 50 #change la taille de la police
"""Si aucun changement n'ont été remarqué lors du changement de ces variables, il est nécessaire d'actualiser la page nuages.html sur le navigateur (f5)"""

