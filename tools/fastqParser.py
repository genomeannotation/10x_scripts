#! /usr/bin/env/ python2.7
#program parses a fastq file and separates into smaller fastq files by barcode
#run with python fastqParser.py -r readgroups.tsv -f file.fastq
#output stores files in ~/fastqFiles/

import argparse
import sys
import os
import gzip
from collections import defaultdict


#Class to create Trie tree
#Currently not used
class Trie:
    def __init__(self):
        self.root = defaultdict()

    def insert(self, word):
        current = self.root
        for letter in word:
            current = current.setdefault(letter, {})
        current.setdefault("_end")

    def search(self, word):
        current = self.root
        for letter in word:
            if letter not in current:
                return False
            current = current[letter]
        if "_end" in current:
            return True
        return False

    def startsWith(self, prefix):
        current = self.root
        for letter in prefix:
            if letter not in current:
                return False
            current = current[letter]
        return True

#function creates directory if none exists, makes a file w/name passed in,  
#if file already exists then does nothing
def makefile(l):
    first = l[:1]
    second = l[1:3]
    third = l[3:7]
    fourth = l[7:11]
    filename1 = 'barcodes/'+first+'/'+second+'/'+third+'/'+fourth+'/%s_r1.fastq' % l
    filename2 = 'barcodes/'+first+'/'+second+'/'+third+'/'+fourth+'/%s_r2.fastq' % l

    #create directory if it does not exist
    if not os.path.exists('barcodes/'+first+'/'+second+'/'+third+'/'+fourth+'/'):
        os.makedirs('barcodes/'+first+'/'+second+'/'+third+'/'+fourth+'/', 0777)

    #open and read file for read 1
    with open(filename1, 'a') as myfile1:
        myfile1.close()

    #open/create file for read 2
    with open(filename2, 'a') as myfile2:
        myfile2.close()

#function writes to fasta file, creates file if does not exist, appends
#to file if it does exist
def writeToFile(b, f):
    first = b[:1]
    second = b[1:3]
    third = b[3:7]
    fourth = b[7:11]
    filename = 'barcodes/'+first+'/'+second+'/'+third+'/'+fourth+'/%s.fastq' % b

    #create directory if it does not exist
    if not os.path.exists('barcodes/'+first+'/'+second+'/'+third+'/'+fourth+'/'):
        os.makedirs('barcodes/'+first+'/'+second+'/'+third+'/'+fourth+'/', 0777)
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
    previous =[" "]
    foundSequence = False
    count = 0

    #arg parse stuff
    parser = argparse.ArgumentParser()
    parser.add_argument('-potentialBarcodes', '-r', help = "Enter the" + \
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
        with gzip.open(args.fastqInput, 'rb') as fqin:
            for line in fqin:
                fields = line.strip().split()
                #checks for start  sequenceV
                if len(fields) > 0 and fields[0].startswith('@'):
                    foundSequence = True
                    if(fields[0] == previous):
                        #checks for barcode, if exists barcode will be used as
                        #filename, esle filename set to discard
                        if len(fields) > 1 and fields[1].startswith('BX:'):
                            barcode = str(cleanBarcode(fields[1])+'_r2')
                            previous =" "
                        else:
                            barcode = '~discard'
                    else:
                        #checks for barcode, if exists barcode will be used as
                        #filename, esle filename set to discard
                        if len(fields) > 1 and fields[1].startswith('BX:'):
                            barcode = str(cleanBarcode(fields[1])+'_r1')
                            previous = fields[0]
                        else:
                            barcode = '~discard'
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
