#!/usr/bin/env python

# Read a sam file with 10x genomics barcode data
# Output the following information:
# - Total # of barcodes
# - Total # of reads
# - Average # of barcodes per sequence/chromosome
# - Average # of reads per sequence/chromosome
# - Sorted list of counts of barcodes per chromosome

import sys
from collections import OrderedDict

def main():
    # Initialize variables
    read_count = 0
    unique_barcodes = set()
    reads_per_seq = {} # map seq_id to total read count for that seq
    barcodes_per_seq = OrderedDict() # map seq_id to a dict that maps barcode to count
    # Read sam file
    for line in sys.stdin:
        read_count += 1
        fields = line.strip().split()
        seq_id = fields[2]
        if seq_id in reads_per_seq:
            reads_per_seq[seq_id] += 1
        else:
            reads_per_seq[seq_id] = 2
        for field in reversed(fields):
            if field.startswith("RX"):
                barcode_field = field
        barcode = barcode_field.split(":")[2]
        unique_barcodes.add(barcode)
        if seq_id in barcodes_per_seq:
            if barcode in barcodes_per_seq[seq_id]:
                barcodes_per_seq[seq_id][barcode] += 1
            else:
                barcodes_per_seq[seq_id][barcode] = 1
        else:
            barcodes_per_seq[seq_id] = {barcode: 1}
    # Calculate and print results
    barcode_count = len(unique_barcodes)
    barcode_counts_per_seq = [sum(x.values()) for x in barcodes_per_seq.values()]
    average_barcode_count_per_seq = \
            sum(barcode_counts_per_seq) / float(len(barcode_counts_per_seq))
    average_read_count_per_seq = \
            sum(reads_per_seq.values()) / float(len(reads_per_seq.values()))
    print("Total reads: {0}".format(read_count))
    print("Total barcodes: {0}".format(barcode_count))
    print("Avg barcodes per seq: {0}".format(average_barcode_count_per_seq))
    print("Avg reads per seq: {0}".format(average_read_count_per_seq))
    print("\nBarcodes per seq:")
    for seq_id, barcode_dict in barcodes_per_seq.items():
        print("{0}\t{1}: {2}".format(seq_id, 
            sum(barcode_dict.values()), sorted([x for x in barcode_dict.values()])))


#########################

if __name__ == "__main__":
    main()
