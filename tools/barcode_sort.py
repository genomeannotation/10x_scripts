#!/usr/bin/env python

import argparse
import sys

from operator import itemgetter

#write list to std out
def printOut(l):
    for i in range(len(l)):
        sys.stdout.write(str(l[i]) + '\n' + '\n')

def removeBX(s):
    return s[5:]

def main():
    fields = []
    barcodes = []
    temp = []
    count = 1
    #argparse declarations
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputFile', '--f', help = "Enter the" + \
                        " of the input file.", type=str, required = True)

    args=parser.parse_args()

    with open(args.inputFile, 'r') as input:
        for line in input:
            
            fields = line.strip().split('\t')
            if len(fields) > 0:
                for i in range (len(fields)):
                    if fields[i].startswith('BX:'):
                        fields.insert(0, fields.pop(i)) 
            barcodes.append(fields)
                #printOut(fields)
        
        #printOut(barcodes)
        temp = sorted(barcodes, key=itemgetter(0))
        printOut(temp)

###############################################################################
if __name__ == '__main__':
    main()
