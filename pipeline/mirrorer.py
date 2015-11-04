#!/usr/bin/env python

# Command line script to read: 
#   - a list of ordered contigs
#   - a table of contig  barcode  position
#   - a list of contig lengths
#
# And output an ordered table like this:
#  contig	reverse_complement?
#  contig_foo	yes
#  contig_bar	no
# etc.

import sys
import argparse
import pdb

PERCENTAGE_OF_SEQ = 0.3 # Defines the "tip" of a seq

def get_barcodes_at_beginning(seq_id, length, barcodes_dict):
    # barcodes_dict maps seq_id to a list of (position, barcode) tuples
    length_to_inspect = int(PERCENTAGE_OF_SEQ*length)
    barcodes = []
    for barcode_tuple in barcodes_dict[seq_id]:
        if barcode_tuple[0] < length_to_inspect:
            barcodes.append(barcode_tuple[1])
    return set(barcodes)

def get_barcodes_at_end(seq_id, length, barcodes_dict):
    # barcodes_dict maps seq_id to a list of (position, barcode) tuples
    length_to_inspect = int(PERCENTAGE_OF_SEQ*length)
    barcodes = []
    for barcode_tuple in barcodes_dict[seq_id]:
        if barcode_tuple[0] > length_to_inspect:
            barcodes.append(barcode_tuple[1])
    return set(barcodes)

def calculate_score(ordered_seqs, seq_lengths, seq_barcodes):
    """Evaluate an ordering/orientation of seqs"""
    score = 0
    # Look at each seq and the seq that follows it
    # Hence iterate up to the second-to-last seq
    for i, seq in enumerate(ordered_seqs[:-1]):
        seq_id = seq[0] 
        reversed = seq[1]
        length = seq_lengths[seq_id]
        next_seq = ordered_seqs[i+1][0]
        next_seq_length = seq_lengths[next_seq]
        next_seq_reversed = ordered_seqs[i+1][1]
        if reversed:
            barcodes = get_barcodes_at_beginning(seq_id, length, seq_barcodes)
        else:
            barcodes = get_barcodes_at_end(seq_id, length, seq_barcodes)
        if next_seq_reversed:
            next_seq_barcodes = get_barcodes_at_end(next_seq,
                    next_seq_length, seq_barcodes)
        else:
            next_seq_barcodes = get_barcodes_at_beginning(next_seq,
                    next_seq_length, seq_barcodes)
        score += len(barcodes & next_seq_barcodes)
    return score



def main():
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('--order-file', '-o', required=True)
    parser.add_argument('--barcode-table', '-b', required=True)
    parser.add_argument('--seq-lengths', '-s', required=True)
    args = parser.parse_args()

    # Read seq_lengths file and store the lengths
    seq_lengths = {}
    with open(args.seq_lengths, 'r') as lengths:
        for line in lengths:
            fields = line.strip().split()
            seq_lengths[fields[0]] = int(fields[1])

    # Read barcode_table, store the info in a dict
    # that maps seq_id to a list of (position, barcode) tuples
    seq_barcodes = {}
    with open(args.barcode_table, 'r') as barcodes:
        for line in barcodes:
            fields = line.strip().split()
            seq_id = fields[0]
            position = int(fields[1])
            barcode = fields[2]
            if seq_id in seq_barcodes:
                seq_barcodes[seq_id].append( (position, barcode) )
            else:
                seq_barcodes[seq_id] = [ (position, barcode) ]

    # Read ordered contigs file, store a list of 
    # [seq_id, reversed] lists where reversed is True/False
    ordered_seqs = []      
    with open(args.order_file, 'r') as orders:
        for line in orders:
            ordered_seqs.append( [line.strip(), False] )

    # Assign a score to the current ordering
    current_score = calculate_score(ordered_seqs, seq_lengths, seq_barcodes)

    # Iterate through ordered seqs. Flip each one and recalculate score
    # If score improves, keep it flipped
    # Stop once an entire pass through the list fails to improve the score
    still_improving = True
    while still_improving:
        #pdb.set_trace()
        made_an_improvement = False
        for seq in ordered_seqs:
            seq[1] = not seq[1] # Flip it
            new_score = calculate_score(ordered_seqs, seq_lengths, seq_barcodes)
            if new_score > current_score:
                current_score = new_score
                made_an_improvement = True
                continue
            else:
                seq[1] = not seq[1] # No improvement; flip it back
        if not made_an_improvement:
            still_improving = False

    # Print results
    for seq in ordered_seqs:
        print("{0}\t{1}".format(seq[0], seq[1]))


##########################

if __name__ == '__main__':
    main()
