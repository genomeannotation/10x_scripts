#program recursively traverses directory and gzips any .fastq file
#run in folder above /barcodes

import os
import fnmatch
import gzip
import shutil

def main():
    os.chdir("barcodes")
    for root, dirs, files in os.walk("."):
        path = root.split('/')
        print (len(path) - 1) *'---' , os.path.basename(root)
        for file in files:
            if file.endswith('.fastq'):
                p = root[1:]
                fi = os.getcwd()+p+'/'+file
                fo = os.getcwd()+p+'/'+file+'.gz'
                with open(fi, 'rb') as f_in, gzip.open(fo, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                os.remove(fi)
            print len(path)*'---', file

###########################################################################
if __name__ == '__main__':
    main()

