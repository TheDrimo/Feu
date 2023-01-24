# usr/bin/env python3

#Labytinthe
"""
Créez un programme qui trouve le plus court chemin entre l’entrée et la sortie 
d’un labyrinthe en évitant les obstacles.
Le labyrinthe est transmis en argument du programme. La première ligne du labyrinthe 
contient les informations pour lire la carte : 
LIGNESxCOLS, caractère plein, vide, chemin, entrée et sortie du labyrinthe. 
Le but du programme est de remplacer les caractères “vide” par des caractères “chemin” 
pour représenter le plus court chemin pour traverser le labyrinthe. 
Un déplacement ne peut se faire que vers le haut, le bas, la droite ou la gauche.
"""

import sys
import os
import string
import numpy as np

def presence_fichier(arguments):
	if len(arguments) != 2 :
		return True
	fichiers = os.listdir()
	for i in arguments[1:] :
		if i not in fichiers:
			return True
	return False

def laby_valide(fichier):
	with open(fichier) as f :
		plateau = f.readlines()
	if len(plateau) < 2 :
		return False
	plateau = [t.strip("\n") for  t in plateau]
	info = plateau[0]
	laby = plateau[1:]
	nb_ligne = len(laby)
	nb_colonne = len(laby[0])
	obstacle = laby[0][0]
	for ligne in laby :
		if len(ligne) != nb_colonne :
			return False
		for c in ligne :
			if c not in [obstacle, "1", "2"] :
				vide = c
	info_reelles = "{}x{}".format(nb_ligne, nb_colonne)+obstacle+vide+"o12"
	if info != info_reelles :
		return False
	return laby

def get_entree_sorties(labyrinthe):
	nb_ligne = len(labyrinthe)
	nb_colonne = len(labyrinthe[0])
	entree = (-1, -1)
	sortie = []
	for y in range(0, nb_ligne):
		for x in range(0, nb_colonne):
			case = labyrinthe[y][x]
			if case == "1" :
				entree = (x, y)
			elif case == "2" :
				sortie.append((x,y))
	return entree, sortie

def resolution(labyrinthe):
	nb_ligne = len(labyrinthe)
	nb_colonne = len(labyrinthe[0])
	entree, sorties = get_entree_sorties(labyrinthe)
	nb_pas_max = nb_ligne * nb_colonne * 10
	chemin_final = [0]*nb_pas_max
	for sortie in sorties :
		reussi = False
		chemin = []
		position_bonhomme = entree
		while len(chemin) < nb_pas_max :
			distance_bonhomme = get_hauteur_case(sortie, position_bonhomme)
			adjacentes = get_cases_adjacentes(labyrinthe, position_bonhomme)
			distances_adjacentes = [(a, get_hauteur_case(sortie, a)) for a in adjacentes]
			distances_adjacentes = adjacente_vs_chemin(distances_adjacentes, chemin)
			position_bonhomme = shortest_distance(distances_adjacentes)[0]
			if position_bonhomme == sortie :
				reussi = True
				break
			chemin.append(position_bonhomme)
		best_chemin = stop_errance(chemin)
		best_chemin = stop_zigzag(best_chemin)
		if (len(best_chemin) <= len(chemin_final)) & (reussi == True) :
			chemin_final = best_chemin
	affichage_chemin(labyrinthe, chemin_final)
	if reussi : 
		print("=> SORTIE ATTEINTE EN {} COUPS !".format(len(chemin_final)))
	elif len(chemin_final) == nb_pas_max :
		print("Arg, ce labyrinthe est trop dur pour moi !")
		print("Même après 1000 pas je n'ai pas trouvé la sortie")

def stop_errance(chemin):
	chemin_plus_court = []
	curseur = 0
	while curseur < len(chemin) :
		chemin_plus_court.append(chemin[curseur])
		curseur += 1
		for i in range(curseur+1, len(chemin)):
			if chemin[i] == chemin[curseur] :
				curseur = i
	return chemin_plus_court

def stop_zigzag(chemin):
	chemin_plus_court = []
	curseur = 0
	while curseur < len(chemin) :
		chemin_plus_court.append(chemin[curseur])
		curseur += 1
		for i in range(curseur, len(chemin)):
			for (a,b) in [(0,-1), (1,0), (0,1), (-1,0)]:
				x, y = chemin[curseur][0]+a, chemin[curseur][1]+b
				if (chemin[i] == (x,y)) & (i - curseur > 2) :
					chemin_plus_court.append(chemin[curseur])
					curseur = i
	return chemin_plus_court

def shortest_distance(coord_case):
	case_ajoutee = coord_case[0]
	for curseur in range(0, len(coord_case)) :
		if coord_case[curseur][1] < case_ajoutee[1] :
			case_ajoutee = coord_case[curseur]
	return case_ajoutee

def adjacente_vs_chemin(coord_case, historique) :
	adjacente = []
	for coord, h in coord_case :
		if coord in historique :
			compte = 0
			for c in historique :
				if c == coord :
					compte += 1
			adjacente.append((coord, round(h+1*compte, 2)))
		else :
			adjacente.append((coord, h))
	return adjacente

def get_hauteur_case(coord_centre, coord_case):
	a = abs(coord_case[0] - coord_centre[0])
	b = abs(coord_case[1] - coord_centre[1])
	c = np.sqrt(a**2 + b**2)
	return round(c, 2)

def get_cases_adjacentes(labyrinthe, coord_case):
	nb_ligne = len(labyrinthe)
	nb_colonne = len(labyrinthe[0])
	case_adjacentes = []
	x,y = coord_case
	for (a,b) in [(0,-1), (1,0), (0,1), (-1,0)] :
		xmove, ymove = -1, -1
		if (x + a < nb_colonne) & (x + a >= 0) & (y + b < nb_ligne) & (y + b >= 0):
			if labyrinthe[y+b][x+a] != "*":
				xmove, ymove = x+a, y+b
				case_adjacentes.append((xmove, ymove))
	return case_adjacentes

def affichage_chemin(labyrinthe, chemin):
	nb_ligne = len(labyrinthe)
	nb_colonne = len(labyrinthe[0])
	figure = ""
	for y in range(0, nb_ligne) :
		for x in range(0, nb_colonne) :
			ajout = labyrinthe[y][x]
			if ((x,y) in chemin) & (ajout not in ["1", "2"]) :
				ajout = "o"
			figure += ajout
		if y != nb_ligne - 1 :
			figure += "\n"
	print(figure)

def affichage(forme):
	fig = ""
	for ligne in forme[:-1] :
		fig += ligne + "\n"
	fig += forme[-1]
	print(fig)

def principal():
	arg = sys.argv
	if presence_fichier(arg) :
		print("error")
		exit()
	laby = laby_valide(arg[1])
	if not laby :
		print("error")
		exit()
	#affichage(laby)
	resolution(laby)

principal()