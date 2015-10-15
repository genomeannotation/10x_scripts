#!/usr/bin/env python

# Command line script to read a sparse matrix and a clusters.txt file
# Then output an ordering for the clusters

import sys
import networkx
import argparse

def main():
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('--sparse-matrix', '-s', required=True)
    parser.add_argument('--clusters', '-c', required=True)
    args = parser.parse_args()

    # Read clusters file, store a list of lists
    clusters = []
    with open(args.clusters, 'r') as clust:
        for line in clust:
            clusters.append(line.strip().split())

    # Read sparse matrix file, store a graph
    all_nodes = networkx.Graph()
    with open(args.sparse_matrix, 'r') as matrix:
        for line in matrix:
            fields = line.strip().split()
            all_nodes.add_edge(fields[0], fields[1], weight=int(fields[2]))

    for cluster in clusters:
        # Create a graph
        g = networkx.Graph()
        for i, node in enumerate(cluster):
            for other_node in cluster[i+1:]:
                if other_node in all_nodes[node]:
                    g.add_edge(node, other_node, weight=all_nodes[node][other_node])

        # Print stuff
        print("cluster {0}:".format(cluster))
        for node in g.nodes():
            print(node)
            print(g[node])
            print("****")


##########################

if __name__ == '__main__':
    main()
