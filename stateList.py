#!/usr/bin/python
#
# NAME & VERSION
#
# 	stateList.py
#	Version 1.1
#
# DESCRIPTION
#
#	Produces a file with a list of states representing one-half inning
#	each on their own line.
#	The program can't tell when a game is over, which essentially means
#	that it's only useful for processing one game at a time.
#
# USAGE
#
# 	./stateList.py input.gs [> output.txt]

import csv
import sys

PROGRAM = "stateList"
VERSION = "1.1"

inputFilename = sys.argv[1]
inputFile = open(inputFilename, "rb")
inputReader = csv.reader(inputFile)

newInning = True
inningTB = None
inningNbr = 0
RUN_CHAR = "-R"

states = []

for row in inputReader:
	if newInning:
		newInning = False
		if inningTB == "T":
			inningTB = "B"
		else:
			inningTB = "T"
			inningNbr += 1
		states = [inningTB + str(inningNbr),row[0]]

	if row[1] == '3000' or row[1] == '----':
		if row[3] == '1':
			states.append(row[1]+RUN_CHAR)
		else:
			states.append(row[1])
		print states
		newInning = True
	else:
		if row[3] == '1':
			states.append(row[1]+RUN_CHAR)
		else:
			states.append(row[1])

inputFile.close()
