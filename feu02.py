# usr/bin/env python3

"""
Créez un programme qui reçoit une expression arithmétique dans une chaîne de caractères
et en retourne le résultat après l’avoir calculé.
Vous devez gérer les 5 opérateurs suivants : “+” pour l’addition, “-” pour la soustraction,
“*” la multiplication, “/” la division et “%” le modulo.
"""

import string
import sys

arg = sys.argv[1]

def formatage(expression):
	expression = expression.replace(" ", "")
	expression = expression.replace("-", "+n")
	expression = expression.replace("nn", "")
	for op in list("*/+%") :
		expression = expression.replace(op+"+", op)
	if expression[0] == "+" :
		expression = expression[1:]
	return expression

def takthemdown(expression):
	res = formatage(expression)
	while "(" in res :
		res = finddeep(res)
	res = calculsansparenthese(res)
	if res[0] == "n":
		res = "-" + res[1:]
	res = float(res)
	if (res-round(res) == 0):
		res = round(res)
	return res

def finddeep(expression):
	searchpar = expression
	while "(" in searchpar :
		searchpar = isoleparenthese(searchpar)
	calcul = calculsansparenthese(searchpar)
	searchpar = "(" + searchpar + ")"
	res = expression.replace(searchpar, str(calcul))
	return res

def isoleparenthese(expression):
	bloc = ""
	record = False
	deep = 0
	for i in expression :
		if i == "(" :
			deep += 1
			record = True
		if i == ")" :
			deep -= 1
		if record == True :
			bloc += i
		if (record == True) & (deep == 0) :
			record = False
			break
	return bloc[1:-1]

def calculsansparenthese(expression):
	res = expression
	for op in list("*/+%") :
		res = thisop(res, op)
	return res

def thisop(expression, op="*"):
	res = expression
	while op in res :
		res = simple(res, op)
		res = formatage(res)
	return res

def simple(expression, op="*"):
	expression = formatage(expression)
	expression_listed = splitexpr(expression)
	formule = ""
	calculstr = ""
	for i in range(0, len(expression_listed)-1):
		gauche = expression_listed[i-1]
		milieu = expression_listed[i]
		droite = expression_listed[i+1]
		formule = gauche + milieu + droite
		if milieu == op :
			calculstr = operation(gauche, milieu, droite)
			break
	res = expression.replace(formule, calculstr)
	return res

def operation(g, m, d):
	calcul = ""
	try :
		if g[0] == "n" :
			g = g.replace("n", "-")
		if d[0] == "n" :
			d = d.replace("n", "-")
		g, d = float(g), float(d)
		if m == "*" :
			calcul = g * d
		elif m == "/" :
			calcul = g / d
		elif m == "+" :
			calcul = g + d
		elif m == "%" :
			calcul = g % d
		if calcul < 0 :
			calcul = "+n" + str(abs(calcul))
		else :
			calcul = str(calcul)
	except :
		pass
	return calcul

def splitexpr(expression):
	expression = formatage(expression)
	for e in ["+", "*", "/", "%"]:
		expression = expression.replace(e, " "+e+" ")
	return expression.split(" ")


print(takthemdown(arg))
