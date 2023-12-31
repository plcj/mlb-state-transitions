#!/usr/bin/python

# whittle.py
# Version 1.0
# 2014 May 18
# by Luke Jordan

# Removes bevent fields 8 and 9 from a .s file
# by copying the file without those fields.
# Fields 8 and 9 are row indexes 4 and 5.

# USAGE
#
# $ ./whittle.py inputFile outputFile

#import argparse
import csv
import sys

#parser = argparse.ArgumentParser()
#args = parser.parse_args()

inputFilename = sys.argv[1]
inputFile = open(inputFilename, 'rb')
inputReader = csv.reader(inputFile)

outputFilename = sys.argv[2]
outputFile = open(outputFilename, 'wb')
outputWriter = csv.writer(outputFile)

for row in inputReader:
    outputWriter.writerow([row[0],row[1],row[2],row[3],
        row[6],row[7],row[8],row[9],row[10],row[11],
        row[12],row[13]])

inputFile.close()
outputFile.close()

