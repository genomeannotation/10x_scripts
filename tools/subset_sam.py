#!/usr/bin/env python

# Read a sam file containing barcoded reads. For each seq/chromosome
# Take a list of seq/chromosome ids and an end_position as 
# command line arguments.
# Output reads that are on one of the seqs/chromosomes specified
# as long as their position is <= the end_position

# Example usage:  
#   samtools view foo.bam | python subset_sam.py --seqlist Chr1,Chr2,Chr3 --end 2000000
# (outputs all reads in the bam file that are from the first 2Mbp of the first 3 chromosomes)

import sys

def main(args):
    if len(args) < 2:
        print("Usage: clusterer.py <end_position> <chromosome 1> <chromosome 2> ... <chromosome N>")
        exit()

    end_pos = int(args[1])
    chromosomes = args[2:]

    for line in sys.stdin:
        fields = line.strip().split()
        if len(fields) < 4:
            continue
        seq_id = fields[2]
        try:
            position = int(fields[3])
        except:
            continue
        if (len(chromosomes) == 0 or seq_id in chromosomes) and position <= end_pos:
            print(line)



#########################

if __name__ == "__main__":
    main(sys.argv)
