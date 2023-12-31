#!/usr/bin/python
# NAME & VERSION
#
# 	s2gs - source to game states
# 	Version 1.0
#
# DESCRIPTION
#
# 	Converts a source (.s) file to a record of game states (filetype .gs)
# 	suitable for construction of the hash that's used by gs2csv for
# 	producing basic game state analysis.
#
# USAGE:
#
#	./s2gs source.s > source.gs
#
# DETAILS
#
# 	Input format (.s)
#
#	 	A bsa source (.s) file is bevent output, specifically, it is
#	 	the output of the bevent call described in bsapp.  As of bsa
#	 	Version 1, a row of a .s file consists of the following:
#
#		Bevent	Field		Input Row
#		Field	Name		Subscript
#		------	-----		---------
#		0	game id 		0
#		2	inning	    	1
#		3	batting team	2
#		4	outs	    	3
#		26	first runner	4
#		27	second runner	5
#		28	third runner	6
#		29	event text  	7
#		34	event type  	8
#		40	outs on play	9
#		78	new game flag	10
#		79	end game flag	11
#
#	Output format (.gs)
#
#		A csv file with four fields per row signifying the
#		following:
#
#	 		state, next-state, transition, scoring-play
#
#		...where state and next-state are two OFST codes.  Transition is
#		the bevent integer code for the event that caused next-state to
#		follow state.  scoring-play may have values 0 or 1, 0 if no runs
#		scored on the play and 1 if at least one run scored.  The number
#		of runs is not tracked.

import collections
import csv
import sys

# <side-effect ridden global variable-eating defs>

def whichWayTo0000():
    global stateQueue, outsOnPlay, endGame
    lastState = stateQueue[1]
    if (((lastState > '1123') and (outsOnPlay == '1')) or
        ((lastState < '2000') and (outsOnPlay == '2')) or
        ((lastState < '1000') and (outsOnPlay == '3'))):
        return '3000'
    elif endGame:
        return '----'
    else:
        return 'iibce'    # intra-inning base clearing event

def updateState(row):
    global o, f, s, t

    if o != row[3]:
        o = row[3]

    if row[4]:
        f = 1
    elif f == 1:
        f = 0

    if row[5]:
        s = 2
    elif s == 2:
        s = 0

    if row[6]:
        t = 3
    elif t == 3:
        t = 0

def updateSupportVars(row):
    global eventText, eventType, outsOnPlay, scoringPlay, endGame
    eventText, eventType, outsOnPlay = row[7], row[8], row[9]
    if (('-H' in eventText) or (eventType == '23')):
        scoringPlay = 1
    else:
        scoringPlay = 0

    if row[11] == "T":
        endGame = 1
    else:
        endGame = 0

# </side-effect ridden global variable-eating defs>

inputFilename = sys.argv[1]
inputFile = open(inputFilename, 'rb')
inputReader = csv.reader(inputFile)

# Legend for understanding variables and row subscripts
# This describes how the bevent fields in a source (.s) file relate to
# this program.
#
# Bevent	Field		Input Row	s2gs
# Field		Name		Subscript	variable
# ------	-----		---------	--------
# 0 		game id		    0
# 2         inning	        1
# 3         batting team	2
# 4         outs            3       o
# 26		first runner	4		f
# 27		second runner	5		s
# 28		third runner	6		t
# 29		event text      7       eventText
# 34		event type      8       eventType
# 40		outs on play    9       outsOnPlay
# 78		new game flag   10
# 79		end game flag   11      endGame

o           = '0'
f           = '0'
s           = '0'
t           = '0'
eventText   = None
eventType   = None
outsOnPlay  = None
endGame     = None
scoringPlay = None

stateQueue = collections.deque(['0000','0000'])

firstRow = 1
inningTerm = None

for row in inputReader:
    if firstRow:
        firstRow = 0
    else:
        updateState(row)
        state = "%s%s%s%s" %(o, f, s, t)
        if state == '0000':
            txnTo0000 = whichWayTo0000()
            if txnTo0000 != 'iibce':
                inningTerm = 1
                stateQueue.append(txnTo0000)
            else:
                stateQueue.append(state)
        else:
            stateQueue.append(state)

        stateQueue.popleft()
        print "%s,%s,%s,%s" %(stateQueue[0], stateQueue[1],\
                eventType, scoringPlay)

        if inningTerm:
            stateQueue[0], stateQueue[1] = '0000', '0000'
            inningTerm = 0
    updateSupportVars(row)

inputFile.close()

sys.stderr.write("The last row of input will not appear in output.\n")
sys.stderr.write("Add it manually.\n")

