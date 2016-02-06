# /usr/bin/env/ python 2.7
# program searches for passed in barcodes and appends them to 2 files
# separate barcodes with spaces
# run with python retrieveBarcodes -b barcode1 barcode2 barcode3 -o outputFileName
import argparse
import sys
import os
import gzip
import shutil

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
                    outfile.write(line)

def gzipFile(outfile):
    with open (outfile, 'rb') as f_in, gzip.open('%s.gz' % outfile, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(outfile)

def main():
    barcodes = []

    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--barcodes', nargs='+', help='Enter barcodes' + \
                        'with space as delimiter', required = True)
    parser.add_argument('-o','--output', help='Name of the output file',
                        type = str, required=True)

    args = parser.parse_args()

    outfile1 = args.output+'_r1.fastq'
    outfile2 = args.output+'_r2.fastq'

    for i in range(len(args.barcodes)):
        l = str(args.barcodes[i])

        first = l[:1]
        second = l[1:3]
        third = l[3:7]
        fourth = l[7:11]

        filename1 = 'barcodes/'+first+'/'+second+'/'+third+'/'+fourth+'/%s_r1.fastq.gz' % l
        filename2 = 'barcodes/'+first+'/'+second+'/'+third+'/'+fourth+'/%s_r2.fastq.gz' % l
        writeToFile(filename1, filename2, args.output)
        print(outfile1, outfile2)
        if os.path.lexists(outfile1):
            gzipFile(outfile1)
        if os.path.lexists(outfile2):
            gzipFile(outfile2)

########################################################################################
if __name__ == '__main__':
    main()
