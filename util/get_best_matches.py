#!/usr/bin/env python

# Read sparse matrix file
# For each contig, output the two most similar contigs

import sys
from collections import OrderedDict

def get_best_matches(contig, contigs_dict):
    # Get list of (other_contig, score) tuples
    matches = list(contigs_dict[contig].items())
    # Sort that list based on score
    matches = sorted(matches, key=lambda x: x[1], reverse=True)
    if len(matches) < 2:
        sys.stderr.write("couldn't find two matches for {0}; skipping\n".format(contig))
        return None, None
    # Return top two results
    return matches[0][0], matches[1][0]

# Create a dict that maps each contig to a {other_contig: score} dict
contigs = OrderedDict()

# Read sparse matrix and store values
with open(sys.argv[1]) as matrix_file:
    for line in matrix_file:
        contig_a, contig_b, score = line.strip().split()
        score = int(score)
        if contig_a in contigs:
            contigs[contig_a][contig_b] = score
        else:
            contigs[contig_a] = {contig_b: score}

# Output each contig's best two matches
print("Contig\tMatch1 (Strength)\tMatch2 (Strength)")
for contig, contig_matches in contigs.items():
    match1, match2 = get_best_matches(contig, contigs)
    if match1 is None:
        continue
    match1_strength = contig_matches[match1]
    match2_strength = contig_matches[match2]
    print("{0}\t{1} ({2})\t{3} ({4})".format(contig, match1,
        match1_strength, match2, match2_strength))
