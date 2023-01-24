# usr/bin/env python3

#Trouver une forme
"""
Créez un programme qui affiche la position de l’élément le plus en haut à droite (dans l’ordre) 
d’une forme au sein d’un plateau.
"""

import sys
import os
import string

arg = sys.argv


def verification_arguments(arguments):
	error = False
	if len(arguments) != 3 :
		error = True
	fichiers = os.listdir()
	for i in arguments[1:] :
		if (i not in fichiers) & (i[-4] != ".txt"):
			error = True
	return error

def chercher(botte, forme):
	botte = [t.strip("\n") for t in botte]
	forme = [t.strip("\n") for t in forme]
	trouve = False
	coordonnees = (-1, -1)
	hauteur_botte = len(botte)
	hauteur_forme = len(forme)
	surfaceforme = 0
	surface = 0
	for yforme in range(0, hauteur_forme) :
		longueur_forme = len(forme[yforme])
		for xforme in range(0, longueur_forme) :
			caseforme = forme[yforme][xforme]
			if caseforme in string.digits :
				surfaceforme += 1
	for y in range(0, hauteur_botte) :
		longueur_botte = len(botte[y])-1
		for x in range(longueur_botte, -1, -1) :
			casebotte = botte[y][x]
			firstforme = forme[0][0]
			if (casebotte == firstforme) & (firstforme in string.digits) :
				here = True
				for yforme in range(0, hauteur_forme) :
					if here == False :
						break
					longueur_forme = len(forme[yforme])
					for xforme in range(0, longueur_forme) :
						if here == False :
							break
						if (y+yforme < hauteur_botte) :
							longueur_botte_forme = len(botte[y+yforme].strip("\r\n"))
							if (x+xforme < longueur_botte_forme) :
								caseforme = forme[yforme][xforme]
								dansbotte = botte[y + yforme][x + xforme]
								if (caseforme == dansbotte) & (dansbotte in string.digits) :
									surface += 1
								if (caseforme != dansbotte) & (caseforme in string.digits) :
									here = False
			if surface == surfaceforme :
				trouve = True
				coordonnees = (x, y)
				return trouve, coordonnees
			else :
				surface = 0
	return trouve, coordonnees

def affichage(botte, forme, coordonnees):
	botte = [t.strip("\n") for t in botte]
	forme = [t.strip("\n") for t in forme]
	hauteur_botte = len(botte)
	figure = ""
	for y in range(0, hauteur_botte) :
		for x in range(0, len(botte[y])) :
			ajout = "-"
			xforme = x - coordonnees[0]
			yforme = y - coordonnees[1]
			hauteur_forme = len(forme)
			if (yforme >= 0) & (yforme < hauteur_forme) :
				longueur_forme, hauteur_forme = len(forme[yforme]), len(forme)
				if (xforme >= 0) & (xforme < longueur_forme) :
					caseforme = forme[yforme][xforme]
					if caseforme in string.digits :
						ajout = caseforme
			figure += ajout
		figure += "\n"
	return figure

def solution(arguments):
	if verification_arguments(arguments) :
		print("error")
		exit()
	plateau_name = arguments[1]
	atrouvee_name = arguments[2]
	with open(atrouvee_name) as f :
		atrouver = f.readlines()
	with open(plateau_name) as f :
		plateau = f.readlines()
	flag, coord = chercher(plateau, atrouver)
	if flag :
		print("Trouvé !")
		print("Coordonnées :", coord)
		print(affichage(plateau, atrouver, coord))
	else :
		print("Introuvable")


solution(arg)




