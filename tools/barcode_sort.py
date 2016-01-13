#!/usr/bin/env python

import argparse
import sys

from operator import itemgetter

#keep track of file
#dict fileList[]

class HashTable:
    #mod hash value
    #modValue = 10
    
    def __init__(self):
        self.keys = [None]
        self.data = [None]

    def insertValue(self, key, data):
        
        #mod hash value
        modValue = 10 

        #generate a new hash value, 
        hashValue = self.hashFunction(key, modValue)

        if self.keys[hashValue] == None:
            self.keys[hashValue] = key
            self.data[hashValue] = data
        else:
            if self.keys[hashValue] == key:
                # key is found, replace current data with new data
                self.data[hashValue] = data
            else:
                #collision occured, rehash a new value
                nextKey = self.rehash(hashValue, modValue)
                while self.keys[nextKey] != None and \
                        self.keys[nextKey] != key:
                    nextKey = self.rehash(nextKey, modValue)
                #if no key is present set key and data
                if self.keys[nextKey] == None:
                    self.keys[nextKey] = key
                    self.data[nextkey] = data
                else:
                    #key is found, replace existing data with new data
                    self.data[nextKey] = data
    
    #Generate a hash value key modulo modValue
    def hashFunction(self, key, modValue):
        return key%modValue
    
    #Generate a new hash value (old value + 1) % moduloValue
    def rehash(self, hashValue, modValue):
        return (hashvalue + 1)%modValue
    
    #Calls hashfunction to find key, if collison occured and key placed 
    #in a rehashed position will call rehash function. Stops when key is found
    #or if returns to initial position.
    def findValue(self, key):
        modValue = 10
        #find initial hash value
        intialPosition = self.hashFunction(key, modValue)
        
        data = None
        found = False
        stop = False
        
        position = initialPosition

        while self.keys[position] != None and not found and \
                not stop:
            #Key is in initial position, data is returned
            if self.keys[position] == key:
                found = True
                data = self.data[position]
            #Key is not in initial position, rehash is called
            else:
                position = self.rehash(position, moduloValue)
                #Key has not been found, the rehashed position
                #has returned to the initial position
                if position == initialPosition:
                    stop = True
        return data
    #Overload the getitem method
    #def __getitem__(self, key):
    #    return self.findValue(key)
    
    #overload the setitem method
    #def __setitem_(self, key, data):
    #    self.insertValue(key, data)

#Prints barcodes to file
def tofile(l):
    
    #Writes reads with same BX: to file
    #ToDo: add hashtable to keep track of files if current code is to slow
    for i in range (len(l)):
        k = l[i];  
        with open('%s.txt' % k[0], 'a') as myFile:              
            temp = l[i]
            myFile.write('@HD' + temp.pop(0) + '\n')
            myFile.write('\t'.join(temp) + '\n')
        myFile.close()

#write list to std out
def printOut(l):
    for i in range(len(l)):
        #to stdout as a list
        #sys.stdout.write(str(l[i]) + '\n' + '\n')
        
        temp = l[i]
        #pops BX barcode, sets as header
        print('@HD ' + temp.pop(0))
        #prints list contents delimited with a tab
        print('\t'.join(temp) + '\n')

# Removes the BX: from barcode
def removeBX(s):
    return s[5:]

def main():
    fields = []
    barcodes = []
    temp = []
    count = 1
    #argparse declarations
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputFile', '-f', help = "Enter the" + \
                        " of the input file.", type = str, required = True)

    args=parser.parse_args()

    with open(args.inputFile, 'r') as input:
        for line in input:
            
            fields = line.strip().split('\t')
            if len(fields) > 1:
                for i in range (len(fields)):
                    if fields[i].startswith('BX:'):
                        fields.insert(0, str(removeBX(fields.pop(i)))) 
                barcodes.append(fields)
                #printOut(fields)
        
        #printOut(barcodes)
        temp = sorted(barcodes, key = itemgetter(0, 1))
        #printOut(temp)
        tofile(temp);
###############################################################################
if __name__ == '__main__':
    main()
