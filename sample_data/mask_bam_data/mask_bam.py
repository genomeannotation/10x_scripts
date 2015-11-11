import csv
import argparse

def Main():
        #bool used to keep track if a value is found
        found = False
        
        #grab the arguments from the command line
        parser = argparse.ArgumentParser()
        parser.add_argument("maxReadCounts", help="The max " + \
                            "number of reads", type=int)
        parser.add_argument("readCountsFile", help="Name of the " + \
                            "input file", type=str)
        args = parser.parse_args()

        #open the output file
        with open('maskOutput.bed', 'a') as outFile:
            
            #open the input file
            with open(args.readCountsFile) as input:
                for line in input:
                    #strip the values and store them in list
                    fields = line.strip().split()

                    #check if counts is above threshold and
                    #start of range has not been found
                    if int(fields[3]) >= args.maxReadCounts \
                            and found == False:
                        found = True
                        
                        #write chr number and start position to outfile
                        outFile.write("%s\t%s" %(fields[0], fields[1]))
                    
                    #end of range has been found
                    elif int(fields[3]) < args.maxReadCounts \
                            and found == True:
                        #write end of range to outfile
                        outFile.write("\t%d\n" %(int(fields[1]) - 1))
                        found = False

            #close input file
            input.close()
        #close output file    
        outFile.close()
if __name__ == '__main__':
    Main()
