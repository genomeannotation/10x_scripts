#! /usr/bin/env/ python2.7
#program parses a fastq file and separates into smaller fastq files by barcode
#run with python fastqParser.py -p potentialReads -f fastqFile
#output stores files in ~/fastqFiles/

import argparse
import sys
import os

#function creates directory if none exists, makes a file w/name passed in,  
#if file already exists then does nothing
def makefile(l):
    filename = '~/fastqFiles/%s.fastq' % l 
    if not os.path.exists('~/fastqFiles/'):
        os.makedirs('~/fastqFiles/', 0777)
    with open(filename, 'a') as myfile:
        myfile.close()

#function writes to fasta file, creates file if does not exist, appends
#to file if it does exist
def writeToFile(b, f):
    filename = '~/fastqFiles/%s.fastq' % b
    if not os.path.exists('~/fastqFiles/'):
        os.makedirs('~/fastqFiles/', 0777)
    for i in range(len(f)):
        temp = f[i]
        with open(filename, 'a') as myfile:
            myfile.write(' '.join(temp) + '\n')
        myfile.close()

#removes first 3 and last 2 chars from file name
def cleanFileName(f):
    return f[3:-2]

#removes first 5 and last 2 chars from file name
def cleanBarcode(b):
    return b[5:-2]

def main():
    fields = []
    temp = []
    foundSequence = False
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
                fields = line.strip().split()
                
                #checks for start  sequence
                if len(fields) > 0 and fields[0].startswith('@'):
                    foundSequence = True
                    
                    #checks for barcode, if exists barcode will be used as
                    #filename, esle filename set to discard
                    if len(fields) > 1 and fields[1].startswith('BX:'): 
                        barcode = str(cleanBarcode(fields[1]))
                    else:
                        barcode = 'discard'
                
                if len(fields) > 0 and foundSequence == True:
                    temp.append(fields)
                
                #writes 4 lines to file
                if len(temp) > 3 and foundSequence == True:
                    writeToFile(barcode, temp)
                    temp[:] = []
                    del barcode
                    foundSequence = False

###############################################################################
if __name__ == '__main__':
    main()
