# /usr/bin/env/ python 2.7
# program searches for passed in barcodes and appends them to 2 files
# separate barcodes with spaces
# run with:
# python retrieveBarcodes -f inputFileName -o outputFileName
# python retrieveBarcodes -b barcode1 barcode2 barcode3 -o outputFileName

import argparse
import sys
import os
import gzip
import shutil

# appends barcodes into files(forward and backward)
def writeToFile(fn1, fn2, out):
    if os.path.lexists(fn1):
        with open('%s_r1.fastq' % out, 'a') as outfile:
            with gzip.open(fn1, 'rb') as infile:
                for line in infile:
                    outfile.write(line)
    if os.path.lexists(fn2):
        with open('%s_r2.fastq' % out, 'a') as outfile2:
            with gzip.open(fn2, 'rb') as infile2:
                for line in infile2:
                    outfile2.write(line)

# gzips the deletes file
def gzipFile(outfile):
    with open (outfile, 'rb') as f_in, gzip.open('%s.gz' % outfile, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(outfile)

def main():
    barcodes = []
    inputBarcodes = []
    
    #argparse stuff
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--barcodes', nargs='+', help='Enter barcodes' + \
                        'with space as delimiter', required = False)
    parser.add_argument('-o','--output', help='Name of the output file',
                        type = str, required=True)
    parser.add_argument('-f','--barcodeFile', help='Name of input file',
                        type = str, required=False)

    args = parser.parse_args()

    # creates outfile names
    outfile1 = args.output+'_r1.fastq'
    outfile2 = args.output+'_r2.fastq'

    # using barcode input
    if args.barcodes:
        for i in range(len(args.barcodes)):
            l = str(args.barcodes[i])

            first = l[:1]
            second = l[1:3]
            third = l[3:7]
            fourth = l[7:11]

            filename1 = 'barcodes/'+first+'/'+second+'/'+third+'/'+fourth+'/%s_r1.fastq.gz' % l
            filename2 = 'barcodes/'+first+'/'+second+'/'+third+'/'+fourth+'/%s_r2.fastq.gz' % l
            writeToFile(filename1, filename2, args.output)
            #print(outfile1, outfile2)

            #gzip output file
            if os.path.lexists(outfile1):
                gzipFile(outfile1)
            if os.path.lexists(outfile2):
                gzipFile(outfile2)
    
    # using fileinput
    if args.barcodeFile:
        with open(args.barcodeFile, 'r') as input:
            for line in input:
                inputBarcodes = line.strip().split('\t')
            
                l = str(inputBarcodes[0])

                first = l[:1]
                second = l[1:3]
                third = l[3:7]
                fourth = l[7:11]

                filename1 = 'barcodes/'+first+'/'+second+'/'+third+'/'+fourth+'/%s_r1.fastq.gz' % l 
                filename2 = 'barcodes/'+first+'/'+second+'/'+third+'/'+fourth+'/%s_r2.fastq.gz' % l
                writeToFile(filename1,filename2, args.output)
                #print(filename1," ",filename2)
            # gzip output file    
            if os.path.lexists(outfile1):
                gzipFile(outfile1)
            if os.path.lexists(outfile2):
                gzipFile(outfile2)


########################################################################################
if __name__ == '__main__':
    main()
