#!/usr/bin/env python

# this script will read a sample sam file from stdin 
# and calculate the "similarity" between
# adjacent windows of the sequence, based on barcodes associated with loci.
# it's meant to help with sketching out a reasonable "similarity" metric and 
# to help characterize the data so we know what to expect.

# toward this latter end, it'll also select random windows and calculate the
# similarity between the chosen window and *all* other windows.

import sys
import random

WINDOW_SIZE = 10000

windows = {} # a dictionary that maps window number to a list of barcodes

for line in sys.stdin:
    fields = line.strip().split()
    seq_id = fields[2]
    position = int(fields[3])
    for field in reversed(fields):
        if field.startswith("RX"):
            barcode_field = field
    barcode = barcode_field.split(":")[2]
    window_number = int(position / WINDOW_SIZE + 1)
    if window_number in windows:
        windows[window_number].add(barcode)
    else:
        windows[window_number] = set([barcode])

# Print a matrix

for window_a, barcodes_a in windows.items():
    for window_b, barcodes_b in windows.items():
        sys.stdout.write(str(len((barcodes_a & barcodes_b)))+'\t')
    sys.stdout.write('\n')
