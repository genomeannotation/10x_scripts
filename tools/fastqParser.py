#! /usr/bin/env/ python2.7
#program parses a fastq file and separates into smaller fastq files by barcode

import argparse
import sys

#function makes a file w/name passed in, 
#if file already exists then does nothing
def makefile(l):
    with open('%s.fastq' % l, 'a') as myfile:
        myfile.close()

#function writes to fasta file, creates file if does not exist, appends
#to file if it does exist
def writeToFile(b, f):
    with open('%s.fastq' % b, 'a') as myfile:
        myfile.write('/t'.join(f) + '\n')
    myfile.close()

#removes first 3 and last 2 chars from file name
def cleanFileName(f):
    return f[3:-2]

#removes first 5 and last 2 chars from file name
def cleanBarcode(b):
    return b[5:-2]

def main():
    fields = []
    barcode = []
    count = 0

    #arg parse stuff
    parser = argparse.ArgumentParser()
    parser.add_argument('-potentialBarcodes', '-p', help = "Enter the" + \
                        " name of file.", type = str, required = False)
    parser.add_argument('-fastqInput', '-f', help = "Enter the" + \
                        " name of fastq file", type = str, required = False)
    args=parser.parse_args()
   
    #exe if potential barcode file is passed as arg
    if args.potentialBarcodes:
        #while file is open strips and cleans barcode for filename
        with open(args.potentialBarcodes, 'r') as input:
            for line in input:
                fields = line.strip().split('\t')
                makefile(str(cleanFileName(fields[1])))                        
                fields[:]=[]

    #exe if a fastq file is passed as arg
    if args.fastqInput:
        with open(args.fastqInput, 'r') as fqin:
            for line in fqin:
                fields = line.strip().split('\t')
                if len(fields) > 1:
                    for i in range (len(fields)):
                        #search for fields that start with BX:
                        if fields[i].startswith('BX:'):
                            barcode = fields
                            writeToFile(str(cleanBarcode(barcode[i])), fields)
                    barcode[:] = []
                    fields[:] = []

###############################################################################
if __name__ == '__main__':
    main()
