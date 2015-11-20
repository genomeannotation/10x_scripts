#!/usr/bin/env python

# Read SAM file from stdin
# Output sparse matrix to stdout:
#    contig_1   contig_2    <connection_strength>
# Where connection_strength = number of common barcodes
# Optionally filter barcodes by read count

import argparse
import sys
from collections import OrderedDict

def main():
    #####################################
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('--window-size', '-w', type=int)
    args = parser.parse_args()
    window_size = args.window_size

    # { window_id : set(barcode) }
    windows = OrderedDict()

    sys.stderr.write("Reading input...\n")
    for line in sys.stdin:
        fields = line.strip().split()
        position = int(fields[3])
        for field in reversed(fields):
            if field.startswith("BX"):
                barcode_field = field
        barcode = barcode_field.split(":")[2].split("-")[0]
        window = position%window_size
        if window in windows:
            windows[window].add(barcode)
        else:
            windows[window] = set([barcode])

    for w, barcodes in windows.items():
        print(format("{0}:\t{1}", w, '\t'.join(list(barcodes))))

####################################################################################################

if __name__ == "__main__":
    main()
