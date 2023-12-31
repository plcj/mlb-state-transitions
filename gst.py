#!/usr/bin/python
#
# NAME & VERSION
#
# 	gst.py: Graphical State Transitions
# 	Version 1.0
#
# DESCRIPTION
#
# 	Text prototype of graphical presentation of state transitions.
# 	Program expects a file created by s2gs.py.
#	The program can't tell when a game is over, so adjust input
#	accordingly.
#
# USAGE
#
# 	./gst.py input.gs [> output.gsv]

import csv
import pickle
import sys

## Serialized dict created by getTxns.py
## Represents all possible state transitions
TRANSITIONS_FILE = "2000_-_2013.csv.txnDict.p"

ALL_STATES = ('0000','0003','0020','0023','0100','0103','0120','0123',
		'1000','1003','1020','1023','1100','1103','1120','1123',
		'2000','2003','2020','2023','2100','2103','2120','2123',
		'3000')
POSSIBLE_STATE_CHAR = "."
IMPOSSIBLE_STATE_CHAR = " "
REALIZED_STATE_CHAR = "x"
PRINT_SEP_CHAR = " "

def initializeGrid():
	"""Return a dictionary that is initialized for grid printing."""
	grid = {}
	for state in ALL_STATES:
		grid[state] = [PRINT_SEP_CHAR]
	return grid

#############
##  Setup  ##
#############
## Open input and prep for reading
inputFilename = sys.argv[1]
inputFile = open(inputFilename, "rb")
inputReader = csv.reader(inputFile)

transitions = pickle.load(open(TRANSITIONS_FILE, "rb"))
grid = initializeGrid()
inningStates = []
newInning = True
topOfInning = False		## Counterintuitively, this starts off False
inningNbr = 0

##################
##  PROCESSING  ##
##################
for row in inputReader:
	## Figure out what inning it is and act appropriately
	if newInning:
		inningStates = [row[0]]
		newInning = False
		if topOfInning:
			topOfInning = False
		else:
			topOfInning = True
			inningNbr += 1

	## Add game states until all the states that occurred in the inning are
	## recorded
	inningStates.append(row[1])

	## When the inning is over, print out the grid based on inningStates
	if row[1] == '3000':
		newInning = True
		for currentState in inningStates:
			grid[currentState][-1] = REALIZED_STATE_CHAR
			if currentState != '3000':
				for nextState in ALL_STATES:
					if nextState in transitions[currentState]:
						grid[nextState].append(POSSIBLE_STATE_CHAR)
					else:
						grid[nextState].append(IMPOSSIBLE_STATE_CHAR)
			else:
				grid[currentState][-1] = REALIZED_STATE_CHAR

		for state in ALL_STATES:
			if state == '0000':
				print
				if topOfInning:
					print "Top",
				else:
					print "Bot",
				print inningNbr
				print

			print state + PRINT_SEP_CHAR,

			for s in grid[state]:
				print s + PRINT_SEP_CHAR,
			print

		grid = initializeGrid()

###############
##  CLEANUP  ##
###############
inputFile.close()
