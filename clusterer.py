#!/usr/bin/env python

import sys
import argparse

def main(args):
    #####################################
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('--sparse-matrix', '-s', required=True)
    parser.add_argument('--number-of-clusters', '-n', required=True, type=int)
    parser.add_argument('--minimum-connection-strength', '-m', type=int)
    args = parser.parse_args()
    minimum_connection_strength = 0
    if args.minimum_connection_strength:
        minimum_connection_strength = args.minimum_connection_strength

    #####################################
    # Input data
    sys.stderr.write("Reading input...\n")
    contig_sim = [] # Contig similarity [(contig_a, contig_b, num_barcodes_in_common)]
    contigs = set() # Set of all contigs

    with open(args.sparse_matrix, 'r') as matrix_file:
        for line in matrix_file:
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
    while len(clusters) > args.number_of_clusters:
        # Get next highest connection
        biggest = None
        for c in range(0, len(contig_sim)):
            cluster_a = contig_clusters[contig_sim[c][0]]
            cluster_b = contig_clusters[contig_sim[c][1]]
            connection_strength = contig_sim[c][2]
            if connection_strength < minimum_connection_strength:
                continue
            if (biggest == None or contig_sim[c][2] > contig_sim[biggest][2]) and cluster_a != cluster_b: 
                biggest = c
        if not biggest:
            sys.stderr.write("No more connections greater than " +
            "{0}; clustering complete.\n".format(minimum_connection_strength))
            break
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
        print("\t".join([c for c in cluster]))


##################################################

if __name__ == "__main__":
    main(sys.argv)
