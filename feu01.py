# usr/bin/env python3

"""Créez un programme qui affiche un rectangle dans le terminal à partir de 2 entiers
donnés en arguments."""

def rectangle(n, m):
    bords = "o"+"-"*(n-2)+"o"*(int(n>1))+"\n"
    milieu = "|"+" "*(n-2)+"|"*(int(n>1))+"\n"
    rect = bords + milieu*(m-2) + bords*(int(m>1))
    return rect
    

import sys

if len(sys.argv) != 3 :
    print("-1")
    exit()

arguments = sys.argv[1:3]

quitter = False
try :
    for i in arguments :
        if (int(i) != float(i)) :
            quitter = True
        if (int(i) <= 0):
            quitter = True
except :
    quitter = True
if quitter :
    print("-1")
    exit()

a, b = int(arguments[0]), int(arguments[1])


resultat = rectangle(a, b)

print(resultat)


