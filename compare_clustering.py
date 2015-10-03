#!/usr/bin/env python

# Reads two clusters.txt files and tells you how similar they are
# File format is from Lachesis software
# Comments (start with '#') are ignored
# Each line is a tab-separated list of contig ids from a single cluster

import sys

def read_cluster_file(filename):
    """Read a clusters.txt file and return a list of clusters.
    Each cluster is a list of contig ids."""
    clusters = []
    with open(filename, 'r') as infile:
        for line in infile:
            if line.startswith("#"):
                continue
            contigs = line.strip().split()
            clusters.append(sorted(contigs)) # sort for easier comparison
    return clusters

def find_most_similar(cluster, other_clusters):
    """Search through other_clusters and return item most similar to cluster"""
    max_in_common = 0
    most_similar = None
    for i, other_cluster in enumerate(other_clusters):
        cluster_set = set(other_cluster)
        common_entries = items_in_common(cluster, other_cluster)
        if common_entries > max_in_common:
            most_similar = other_cluster
    return most_similar

def items_in_common(cluster_a, cluster_b):
    """Return the number of common items between two clusters"""
    set_a = set(cluster_a)
    set_b = set(cluster_b)
    return len(set_a & set_b)

def main():
    if len(sys.argv) != 3:
        sys.stderr.write("usage: compare_clusters.py <clusters1.txt> <clusters2.txt>\n")
        sys.exit()
    clusterfile1 = sys.argv[1]
    clusterfile2 = sys.argv[2]
    clusters1 = read_cluster_file(clusterfile1)
    clusters2 = read_cluster_file(clusterfile2)
    for i, cluster in enumerate(clusters1):
        most_similar = find_most_similar(cluster, clusters2)
        common_contigs = items_in_common(cluster, most_similar)
        print("Cluster %s:%d has %d/%d items in common with its most similar cluster"
                % (clusterfile1, i, common_contigs, len(cluster)))


##########################

if __name__ == '__main__':
    main()
