#!/usr/bin/env python

import sys

def main(args):
    if len(args) < 2:
        print("Usage: clusterer.py <num_clusters>")
        exit()

    desired_cluster_count = int(args[1])

    #####################################
    # Input data

    sys.stderr.write("Reading input...\n")

    contig_sim = [] # Contig similarity [(contig_a, contig_b, num_barcodes_in_common)]
    contigs = set() # Set of all contigs

    for line in sys.stdin:
        # Skip commented lines
        if line.startswith("#"):
            continue
        contig_a, contig_b, barcodes_in_common = line.strip().split("\t")
        contig_sim.append((contig_a, contig_b, int(barcodes_in_common)))
        contigs.add(contig_a)
        contigs.add(contig_b)
    
    #####################################
    # Clustering

    sys.stderr.write("Clustering contigs...\n")

    clusters = []
    contig_clusters = {} # Maps each contig to its corresponding cluster

    # Initialize every contig as being in its own cluster
    for contig in contigs:
        clusters.append(set([contig]))
        contig_clusters[contig] = clusters[-1]
    
    # Cluster all the things
    while len(clusters) > desired_cluster_count:
        # Get next highest connection
        biggest = 0
        for c in range(1, len(contig_sim)):
            if contig_sim[c][2] > contig_sim[biggest][2]:
                biggest = c
        contig_a = contig_sim[biggest][0]
        contig_b = contig_sim[biggest][1]
        contig_sim.pop(biggest)

        cluster_a = contig_clusters[contig_a]
        cluster_b = contig_clusters[contig_b]

        # Create the new merged cluster
        new_cluster = cluster_a.union(cluster_b)

        # Remove the old clusters
        clusters.remove(cluster_a)
        clusters.remove(cluster_b)
        
        # Add the new cluster
        clusters.append(new_cluster)

        # Set the all of the contigs to be in the new cluster
        for contig in new_cluster:
            contig_clusters[contig] = clusters[-1]

    #####################################
    # Output

    sys.stderr.write("Writing output...\n")

    for cluster in clusters:
        print(cluster)


##################################################

if __name__ == "__main__":
    main(sys.argv)
