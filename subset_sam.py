#!/usr/bin/env python

# Read a sam file containing barcoded reads. For each seq/chromosome
# Take a list of seq/chromosome ids and an end_position as 
# command line arguments.
# Output reads that are on one of the seqs/chromosomes specified
# as long as their position is <= the end_position

# Example usage:  
#   samtools view foo.bam | python subset_sam.py --seqlist Chr1,Chr2,Chr3 --end 2000000
# (outputs all reads in the bam file that are from the first 2Mbp of the first 3 chromosomes)

def main():
    pass


#########################

if __name__ == "__main__":
    main()
