#!/usr/bin/python
#
# NAME & VERSION
#
# 	getTxns.py
# 	Version 1.0
#
# DESCRIPTION
#
#   Create and store a dictionary of state transitions given a file
#   created by gs2csv with option -t (works as of gs2csv 1.0). Only
#   transitions are stored (not counts). The original intent is to
#   record which states may possibly follow each state, which is a
#   feature of the visual representation of state transitions
#   produced by gst (gst uses this program's output).
#
# USAGE
#
# 	./getTxns.py input.csv
#
#   File "input.csv.txnDict.p" is created and contains a serialized dictionary
#   of state transitions.

import csv
import pickle
import sys

inputFilename = sys.argv[1]
inputFile = open(inputFilename, 'rb')
inputReader = csv.reader(inputFile)

possibleTxns = {}

states = ('0000','0003','0020','0023','0100','0103','0120','0123',
          '1000','1003','1020','1023','1100','1103','1120','1123',
          '2000','2003','2020','2023','2100','2103','2120','2123',
          '3000')

# create dict of possible transitions
for row in inputReader:
    if row:
        rowIndex = 0
        s1 = row[0].replace("'","")
        if s1 in states:
            possibleTxns[s1] = []
            for item in row:
                if rowIndex > 0 and rowIndex < 26:
                    if item is not '0':
                        possibleTxns[s1].append(states[rowIndex-1])
                rowIndex += 1

inputFile.close()

# store result
pickle.dump(possibleTxns, open(inputFilename+"txnDict.p", "wb"))

print "Processing successful.  Pickle file written:", inputFilename+".txnDict.p"

##  debug only
#for k in possibleTxns.keys():
#    print k, ":", possibleTxns[k]

