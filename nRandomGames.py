#!/usr/bin/python
#
# NAME & VERSION
#
#	nRandomGames.py
#	1.0
#
# DESCRIPTION
#
#	Print n random games from a serialized list of games.
#
# USAGE
#
# 	./nRandomGames.py input.s.p n

import pickle
import random
import sys

PROGRAM = "nRandomGames"
VERSION = "1.0"

games = pickle.load(open(sys.argv[1], "rb"))
nbrOfGames = int(sys.argv[2])

if nbrOfGames > 0:
	upperBound = len(games) - 1
	while nbrOfGames > 0:
		print games[random.randint(0, upperBound)]
		nbrOfGames -= 1
else:
	print "Number of games must be greater than zero. Given:", nbrOfGames

