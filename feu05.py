# usr/bin/env python3

#Trouver le plus grand carré

"""
Créez un programme qui remplace les caractères vides par des caractères plein 
pour représenter le plus grand carré possible sur un plateau. 
Le plateau sera transmis dans un fichier. 
La première ligne du fichier contient les informations pour lire la carte : 
nombre de lignes du plateau, caractères pour “vide”, “obstacle” et “plein”.
"""

import sys
import os
import string

def presence_fichier(arguments):
	if len(arguments) != 2 :
		return True
	fichiers = os.listdir()
	for i in arguments[1:] :
		if i not in fichiers:
			return True
	return False

def carte_valide(fichier):
	with open(fichier) as f :
		plateau = f.readlines()
	if len(plateau) < 2 :
		return False
	plateau = [t.strip("\n") for  t in plateau]
	info = plateau[0]
	try :
		n = ""
		for i in info :
			if i in string.digits :
				n += i
			else :
				break
		nb_ligne = int(n)
		vide = info[-3]
		obstacle = info[-2]
		plein = info[-1]
	except :
		return False
	carte = plateau[1:]
	hauteur = 0
	for i in carte :
		if (vide in i) | (obstacle in i) :
			hauteur += 1
	if abs(hauteur - nb_ligne) > 2 :
		return False
	for ligne in carte :
		if len(ligne) != len(carte[0]) :
			return False
		for c in ligne.strip("\n") :
			if c not in [vide, obstacle, plein] :
				return False
	return True

def carte_formate(fichier) :
	with open(fichier) as f :
		plateau = f.readlines()
	info = plateau[0]
	vide = "."
	obstacle = "x"
	plein = "o"
	carte = plateau[1:]
	hauteur = 0
	for i in carte :
		if (vide in i) | (obstacle in i) :
			hauteur += 1
	figure = []
	for ligne in carte :
		fig = ""
		for c in ligne :			
			if c == vide :
				fig += "."
			elif c == obstacle :
				fig += "x"
			elif c == plein :
				fig += "o"
		figure.append(fig)
	return figure

def resolution(plateau) :
	hauteur = len(plateau)
	largeur = len(plateau[0])
	taille_max = 1
	coord = (hauteur, largeur)
	#print(largeur, hauteur)
	for i in range(hauteur-1, -1, -1):
		for j in range(largeur-1, -1, -1):
			caractere = plateau[i][j]
			if caractere == "." :
				for t in range(taille_max, largeur):
					carre = extraire_un_carre_du_plateau(plateau, (i,j), t)
					if nombre_obstacles(carre) == 0 :
						if t >= taille_max :
							taille_max = t
							coord = (i, j)
					else :
						break
	carre_final = [["o"*taille_max]]*taille_max
	#print(coord, taille_max)
	affichage_forme_dans_carte(plateau, carre_final, coord)

def extraire_un_carre_du_plateau(plateau, coord, taille):
	x, y = coord
	fig = []
	for i in range(x, x+taille):
		ligne = ""
		for j in range(y, y+taille):
			caratere = "x"
			if (i < len(plateau)) & (j < len(plateau[0])) :
				caratere = plateau[i][j]
			ligne += caratere
		fig.append(ligne)
	return fig

def nombre_obstacles(forme) :
	nb_obstacles = 0
	for ligne in forme :
		for caratere in ligne :
			if (caratere == "x") :
				nb_obstacles += 1
	return nb_obstacles

def affichage_carte(plateau) :
	fig = ""
	for p in plateau[:-1] :
		fig += p + "\n"
	fig += plateau[-1]
	print(fig)

def affichage_forme_dans_carte(botte, forme, coordonnees):
	hauteur_botte = len(botte)
	largeur_botte = len(botte[0])
	taille = len(forme)
	figure = ""
	b, a = coordonnees
	for y in range(0, hauteur_botte) :
		for x in range(0, largeur_botte) :
			ajout = botte[y][x]
			if (y >= b) & (y < b + taille) & (x >= a) & (x < a + taille) :
				if ajout != "x" :
					ajout = "o"
			figure += ajout
		figure += "\n"
	print(figure)

def principal():
	arg = sys.argv
	if presence_fichier(arg) :
		print("error")
		exit()
	if not carte_valide(arg[1]) :
		print("error")
		exit()
	carte = carte_formate(arg[1])
	resolution(carte)

principal()
