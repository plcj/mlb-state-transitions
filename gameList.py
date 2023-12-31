#!/usr/bin/python
#
# NAME & VERSION
#
#	gameList.py
#	1.0
#
# DESCRIPTION
#
#	Produces and serializes a list of game ids from a .s file.
#
# USAGE
#
# 	./gameList.py input.s
#
#   File "input.s.gameList.p" is created and contains a serialized list
#   of game ids.

import csv
import pickle
import sys

PROGRAM = "gameList"
VERSION = "1.0"

inputFilename = sys.argv[1]
inputFile = open(inputFilename, "rb")
inputReader = csv.reader(inputFile)

game = None
games = []

# create game list
for row in inputReader:
    if game != row[0]:
		game = row[0]
		games.append(game)

inputFile.close()

# store result
pickle.dump(games, open(inputFilename+"gameList.p", "wb"))
print "Processing successful.  Pickle file written:", inputFilename+"gameList.p"

