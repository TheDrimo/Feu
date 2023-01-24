# usr/bin/env python3

#Sudoku
"""
Créez un programme qui trouve et affiche la solution d’un Sudoku.
"""

import sys
import os
import string

arg = sys.argv


def presence_fichier(arguments):
	error = False
	if len(arguments) != 2 :
		error = True
	fichiers = os.listdir()
	for i in arguments[1:] :
		if (i not in fichiers) & (i[-4] != ".txt"):
			error = True
	return error

def validite_grille(grille):
	valide = True
	if len(grille) != 9 :
		valide = False
	else :
		for i in grille :
			ligne = i.strip("\n")
			if len(ligne) != 9 :
				valide = False
			else :
				for n in ligne :
					if (n not in string.digits + ".") :
						valide = False
						break
					if (n in string.digits) & (ligne.count(n) != 1) :
						valide = False
						break
	return valide

def get_tranche(grille, num=0, ax=0):
	tranche = ""
	if ax == 0 :
		tranche = grille[num].strip("\n")
	else :
		for i in grille :
			tranche += i[num]
	"""if len(tranche) != 9 :
					print("error")
					exit()"""
	return tranche

def get_col_pos(pos_grille, num) :
	col = []
	for i in pos_grille :
		col.append(i[num])
	return col

def get_carre(grille, coord = (0, 0), num = 0):
	carre = ""
	tous_carres = [(0,0), (0,3), (0,6), (3,0), (3,3), (3,6), (6,0), (6,3), (6,6)]
	y0, x0 = tous_carres[num]
	if coord != (0, 0) :
		a, b = coord
		x0, y0 = a//3*3, b//3*3
	for y in range(y0, y0+3):
		for x in range(x0, x0+3) :
			carre += grille[y][x]
	return carre

def get_pos_carre(pos_sudok, coord = (0, 0), num = 0):
	pos_carre = []
	tous_carres = [(0,0), (0,3), (0,6), (3,0), (3,3), (3,6), (6,0), (6,3), (6,6)]
	y0, x0 = tous_carres[num]
	if (coord != (0, 0)) :
		a, b = coord
		x0, y0 = a//3*3, b//3*3
	for y in range(y0, y0+3):
		for x in range(x0, x0+3) :
			pos_carre.append(pos_sudok[y][x])
	return pos_carre

def chiffre_manquant(suite_nombres):
	manquant = ""
	for i in string.digits :
		if (i not in suite_nombres) & (i != "0") :
			manquant += i
	return manquant

def char_recurrent(list_de_manquants):
	manquant = ""
	for t in list_de_manquants[0] :
		dans_les_trois = True
		for m in list_de_manquants :
			if t not in m :
				dans_les_trois = False
		if dans_les_trois :
			manquant += t
	return manquant

def case_controle(grille, x, y):
	colonne = get_tranche(grille, x, 1)
	ligne = get_tranche(grille, y, 0)
	groupe = get_carre(grille, (x,y))
	manquants = [chiffre_manquant(t) for t in [colonne, ligne, groupe]]
	solution_case = char_recurrent(manquants)
	return solution_case

def unique_char(list_text, char):
	unique = True
	compte = 0
	for t in list_text :
		if char in t :
			compte += 1
	if compte != 1 :
		unique = False
	return unique

def parcourir(grille):
	pos_grille = []
	nb_changement = 0
	for y in range(0, 9) :
		pos_lig = []
		for x in range(0, 9):
			chiffre = grille[y][x]
			if chiffre == "." :
				pos_case = case_controle(grille, x, y)
				pos_lig.append(pos_case)
			else :
				pos_lig.append(chiffre)
		pos_grille.append(pos_lig)
	for y in range(0, 9) :
		for x in range(0, 9) :
			chiffre = grille[y][x]
			resolution_de_la_case = "."
			if chiffre == "." :
				pos_lig = pos_grille[y]
				pos_col = get_col_pos(pos_grille, x)
				pos_car = get_pos_carre(pos_grille, (x, y))
				possibilite_simple = case_controle(grille, x, y)
				if len(possibilite_simple) == 1 :
					resolution_de_la_case = possibilite_simple
				else :
					for p in possibilite_simple :
						if unique_char(pos_lig, p) :
							resolution_de_la_case = p
						if unique_char(pos_col, p) :
							resolution_de_la_case = p
				grille[y] = grille[y][0:x] + resolution_de_la_case + grille[y][x+1:]
				if resolution_de_la_case != "." :
					nb_changement += 1
					#print(resolution_de_la_case)
		#if (y == 8) : print(y, pos_lig)
	"""figure = ""
				for i in pos_grille :
					for j in i :
						figure += j + "_"*(9-len(j))
					figure += "\n"
				print(figure)"""
	return grille, nb_changement

def resolution(grille):
	nb_modification = 1
	while nb_modification != 0 :
		grille, nb_modification = parcourir(grille)
		#affichage(grille)
	return grille

def affichage(grille):
	figure = ""
	for i in grille :
		figure += i
	print(figure)
	if '.' in figure :
		print("Ce Sudoku est trop difficile pour moi !")

def main(arguments):
	if presence_fichier(arguments) :
		print("error")
		exit()
	with open(arguments[1]) as f :
		sudoku = f.readlines()
	if validite_grille(sudoku) == False :
		print("error")
		exit()
	else :
		sudoku = resolution(sudoku)
		affichage(sudoku)

main(arg)