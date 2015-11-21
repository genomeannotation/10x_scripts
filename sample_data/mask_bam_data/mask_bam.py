#!/usr/bin/env python

import argparse

# find the average of 10 read counts takes a list an arg.
def findAverage(l):
    newList = []
    avg = 0
    total = 0
    if len(l) > 9:
        for x in range(0, 10):
            newList = l[x]
            total = total + int(newList[3])
            avg = total/10
    elif len(l) < 10:
        n = len(l) - 1
        for x in range(0, n):
            newList = l[x]
            total = total + int(newList[3])
            avg = total/n
    return avg

# finds a window of 10 values in which the avg is below the 
# specified minReadCount, take a list and minRead value as arg 
# returns retuns a list
def pastLowerBound(l, minRead):
    lowerBound = False
    newList = []
    i = len(l) - 1
    while lowerBound == False:
        for x in range(0, 10):
            if i <= 0:
                break
            else:
                newList.append(l[i])
                i = i - 1
        if int(findAverage(newList)) <= minRead:
            lowerBound = True
            newList = l
        elif i == 0 or i >= len(l):
            newList = l
            break
    return newList[i]
    
# finds a window of 10 values in which the avg is below the 
# specified minReadCount, take a list and minRead value as arg 
# returns a list and bool 
def futureLowerBound(l, minRead):
    lowerBound = False #bool for loop control
    newList = []
    i = len(l) - 1
    while lowerBound == False:
        avg = findAverage(l)
        #if average is below minRead set lowerBound to true, newList to l
        if int(avg) < minRead:
            lowerBound = True
            newList = l
        #if end of list set newList to l and lowerBound to true
        elif i == 0 or i >= len(l):
            newList = l
            i = len(l) - 1
            lowerBound = True
        else:
            i = i - 1
    return (newList[i], lowerBound)

def Main():
        #bools used for flow control
        pastLowerFound = False
        futureLowerFound = False
        found = False
        #list used to store input
        reads = []
        arr = []

        #argparse decalrations
        parser = argparse.ArgumentParser()
        parser.add_argument("minReadCount", help="The lower " + \
                            "threshold for reads", type=int)
        parser.add_argument("maxReadCount", help="The upper  " + \
                            "threshold for reads", type=int)
        parser.add_argument("readCountFile", help="Name of the " + \
                            "input file", type=str)
        args = parser.parse_args()

        #opens output file maskOutput.bed
        with open('maskOutput.bed', 'a') as outFile:
            #reads in input file
            with open(args.readCountFile) as input:
                count = 0
                for line in input:
                    fields = line.strip().split()
                    reads.append(fields)
                    count = count + 1
                    #read above max threshold has been found, 
                    if int(fields[3]) >= args.maxReadCount \
                            and pastLowerFound == False:
                        #check for lower bound the has been read in    
                        arr = pastLowerBound(reads, args.minReadCount)
                        pastLowerFound = True
                        count = 0
                        outFile.write("%s\t%s" %(arr[0], (int(arr[1]))))
                    #past lower bound has been found    
                    elif pastLowerFound == True and count == 10:
                        #check new values read in for lower bound
                        arr, futureLowerFound = futureLowerBound(reads, args.minReadCount)
                        if futureLowerFound == True:
                            outFile.write("\t%d\tmask\n" %(int(arr[1])))
                        else:
                            break
                    #both past and future lowerbounds have been found reset bools and list        
                    if pastLowerFound == True and futureLowerFound == True:
                        reads = []
                        pastLowerFound = False
                        futureLowerFound = False
            input.close()
        outFile.close()

###############################################################################
if __name__ == '__main__':
    Main()

