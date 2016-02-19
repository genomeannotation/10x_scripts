#!/usr/bin/env/ python
#program finds bx barcodes in specifed window in sam file
#sorts and removes duplicates and sends to std out.

#run with:
#python bx_finder.py --windowSize -w --inputfile -f > outputFile 

import argparse
import sys

#prints barcodes to stdout
def printOut(barcodes):
    #sort and remove duplicates
    barcodes = sorted(set(barcodes))
    #send to standard out
    sys.stdout.write(str(barcodes)) 
    sys.stdout.write('\n' + '\n')

def main():
    
    barcodes = []
    count = 0

    #argparse declarations
    parser = argparse.ArgumentParser()
    parser.add_argument('--windowSize', '-w',help="Enter" + \
                                        "  the size of the window.", 
                                        type=int, required = True)
    parser.add_argument('--inputFile', '-f',help="Enter" + \
                                        " the name of the input file.", 
                                        type=str, required = True)
    args=parser.parse_args()
    
    with open(args.inputFile, 'r') as input:
         for line in input:             
            #if the current count == the window size print list
            #to standard out
            if count == args.windowSize:
                #print bacodes to std out 
                printOut(barcodes)
                #clear list
                barcodes[:] = []
                #reset count
                count = 0

            #read line into list
            fields = line.strip().split('\t')
            #if field exist find barcode
            if fields[0]:
                #Search for barcode, not always in same field.
                for i in range(len(fields)):
                    if fields[i].startswith('BX:'):
                        barcodes.append(fields[i])
                        count = count + 1
    
    #If less than specifed window size
    #print barcodes to output
    if len(barcodes) > 0:
        #print out 
        printOut(barcodes)
        #clear list
        barcodes[:] = []
        #reset count
        count = 0

    #close the input file
    input.close()


###############################################################################
if __name__ == '__main__':
    main()
