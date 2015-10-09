#!/usr/bin/env python

# Read SAM file from stdin
# Output sparse matrix to stdout:
#    contig_1   contig_2    <connection_strength>
# Where connection_strength = number of common barcodes
# Optionally filter barcodes by read count

import sys
from collections import OrderedDict

# Look for optional command line arg
min_read_count = 0
if len(sys.argv) > 1:
    min_read_count = int(sys.argv[1])

# Store contigs in a dict that maps contig id to a {barcode: read_count} dict
contigs = OrderedDict()

sys.stderr.write("Reading input...\n")
for line in sys.stdin:
    fields = line.strip().split()
    seq_id = fields[2]
    position = int(fields[3])
    for field in reversed(fields):
        if field.startswith("BX"):
            barcode_field = field
    barcode = barcode_field.split(":")[2].split("-")[0]
    if seq_id in contigs:
        if barcode in contigs[seq_id]:
            contigs[seq_id][barcode] += 1
        else:
            contigs[seq_id][barcode] = 1
    else:
        # Add seq_id to the dictionary
        contigs[seq_id] = {barcode: 1}

# Filter results (optional)
if min_read_count > 0:
    sys.stderr.write("Filtering barcodes based on read count...\n")
    for contig, barcode_dict in contigs.items():
        # Decide which of this contig's barcodes to remove
        barcodes_to_remove = []
        for barcode, read_count in barcode_dict.items():
            if read_count < min_read_count:
                barcodes_to_remove.append(barcode)
        # Now remove them
        for barcode in barcodes_to_remove:
            del barcode_dict[barcode]

# Print a sparse matrix
sys.stderr.write("Writing sparse matrix...\n")
all_contigs = contigs.keys()
for i, contig in enumerate(all_contigs):
    for other_contig in all_contigs[i+1:]:
        barcodes_a = set(contigs[contig].keys())
        barcodes_b = set(contigs[other_contig].keys())
        barcodes_in_common = len((barcodes_a & barcodes_b))
        if barcodes_in_common > 0:
            print("\t".join([contig, other_contig, str(barcodes_in_common)]))
