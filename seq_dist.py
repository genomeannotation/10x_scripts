#!/usr/bin/env python

import argparse
import math
import sys
from util.sequence import Sequence, read_fasta

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fasta', '-f', required=True)
    args = parser.parse_args()

    seqs = None
    with open(args.fasta, 'r') as fasta:
        seqs = read_fasta(fasta) # { header : Sequence }

    if seqs == None:
        sys.stderr.write("ERROR: Failed to read input fasta\n")
        exit(1)

    #####################################################################

    seq_lengths = [len(c.bases) for c in seqs.values()]

    mean = sum(seq_lengths)/len(seq_lengths)
    deviations = [(c-mean)*(c-mean) for c in seq_lengths]
    variance = sum(deviations)/len(deviations)
    stddev = math.sqrt(variance)

    sys.stderr.write("mean:\t"+str(mean)+"\n")
    sys.stderr.write("stddev:\t"+str(stddev)+"\n")

    #####################################################################

    counts = {} # { len_bin : count }
    for header, seq in seqs.items():
        seq_len = len(seq.bases)
        len_bin = int(seq_len / 5000)*5000
        if len_bin in counts:
            counts[len_bin] += 1
        else:
            counts[len_bin] = 1

    for len_bin, count in counts.items():
        print(str(len_bin)+"\t"+str(count))

#################################################################

if __name__ == "__main__":
    main()
