#!/usr/bin/env python

import sys
import argparse
import heapq

def main(args):
    #####################################
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('--sparse-matrix', '-s', required=True)
    parser.add_argument('--number-of-clusters', '-n', required=True, type=int)
    parser.add_argument('--minimum-connection-strength', '-m', type=int)
    parser.add_argument('--merge-progression', '-p', dest='merge_progression', action='store_true')
    parser.set_defaults(merge_progression=False)
    args = parser.parse_args()
    minimum_connection_strength = 0
    merge_progression = args.merge_progression
    if args.minimum_connection_strength:
        minimum_connection_strength = args.minimum_connection_strength

    print(merge_progression)

    #####################################
    # Input data
    sys.stderr.write("Reading input...\n")
    contig_sim = [] # Contig similarity [(contig_a, contig_b, num_barcodes_in_common)]
    contigs = set() # Set of all contigs
    edge_counts = {} # { contig : edge_count }

    with open(args.sparse_matrix, 'r') as matrix_file:
        for line in matrix_file:
            # Skip commented lines
            if line.startswith("#"):
                continue
            contig_a, contig_b, barcodes_in_common = line.strip().split("\t")
            barcodes_in_common = int(barcodes_in_common)

            if contig_a not in edge_counts:
                edge_counts[contig_a] = 1
            else:
                edge_counts[contig_a] += 1
            if contig_b not in edge_counts:
                edge_counts[contig_b] = 1
            else:
                edge_counts[contig_b] += 1

            if barcodes_in_common < minimum_connection_strength:
                continue
            contig_sim.append((contig_a, contig_b, barcodes_in_common))
            contigs.add(contig_a)
            contigs.add(contig_b)

    #####################################
    # Filtering

    sys.stderr.write("Filtering...\n")

    contigs_to_remove = []
    avg_edge_count = sum(edge_counts.values())/len(edge_counts)
    sys.stderr.write("avg edge count: {0}".format(avg_edge_count))
    for contig, edge_count in edge_counts.items():
        if edge_count > 1.5*avg_edge_count:
            sys.stderr.write("Removing overly connected contig {0} with {1} edges\n".format(contig, edge_count))
            contigs_to_remove.append(contig)

    for contig in contigs_to_remove:
        contigs.remove(contig)

    filtered_contig_sim = []
    for edge in contig_sim:
        if edge[0] not in contigs_to_remove and edge[1] not in contigs_to_remove:
            filtered_contig_sim.append(edge)

    sys.stderr.write("Filtered {0}% of edges\n".format(len(filtered_contig_sim)/len(contig_sim)))
    contig_sim = filtered_contig_sim

    #####################################
    # Clustering
    sys.stderr.write("Clustering contigs...\n")
    clusters = []
    contig_clusters = {} # Maps each contig to its corresponding cluster

    # Initialize every contig as being in its own cluster
    for contig in contigs:
        clusters.append(set([contig]))
        contig_clusters[contig] = clusters[-1]

    # Get the n-1 highest connections
    # NOTE: len(contigs)*2 is a hack because we don't know exactly how many connections we'll need.
    # This is because connections between contigs that are already in the same cluster have to be
    # skipped.
    highest = heapq.nlargest(len(contig_sim), contig_sim, key=lambda x: x[2])
        
    # Cluster all the things
    c = 0
    while len(clusters) > args.number_of_clusters:
        # Get next highest connection
        if c >= len(highest):
            sys.stderr.write("No more connections, aborting\n")
            break
        biggest = highest[c]
        c += 1
        contig_a = biggest[0]
        contig_b = biggest[1]

        cluster_a = contig_clusters[contig_a]
        cluster_b = contig_clusters[contig_b]

        if cluster_a == cluster_b:
            continue

        if merge_progression:
            sys.stderr.write("Merging clusters with connection strength: "+str(biggest[2])+"\n")

        if contig_a[:5] != contig_b[:5]:
            sys.stderr.write("Incorectly joining chromosomes {0}: {1} and {2}\n".format(str(c), contig_a, contig_b))

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
