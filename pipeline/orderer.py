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

    for i, cluster in enumerate(clusters):
        # Create a graph
        g = networkx.Graph()
        for j, node in enumerate(cluster):
            for other_node in cluster[j+1:]:
                if other_node in all_nodes[node]:
                    g.add_edge(node, other_node, weight=all_nodes[node][other_node])

        # Find strongest path
        # Create yet another graph, add all nodes from g
        strongest_path = networkx.Graph()
        for node in g.nodes():
            strongest_path.add_node(node)
        # Sort edges in this cluster according to weight
        all_edges = []
        for edge in g.edges():
            node1 = edge[0]
            node2 = edge[1]
            weight = all_nodes[node1][node2]['weight']
            all_edges.append( (node1, node2, weight) )
        all_edges = sorted(all_edges, key=lambda x: x[2], reverse=True)
        # Iterate through edges from strongest to weakest
        for edge in all_edges:
            node1 = edge[0]
            node2 = edge[1]
            weight = all_nodes[node1][node2]['weight']
            node1_edge_count = len(strongest_path[node1])
            node2_edge_count = len(strongest_path[node2])
            # Connect nodes in strongest_path if neither has > 1 edge already
            if node1_edge_count <= 1 and node2_edge_count <= 1:
                strongest_path.add_edge(node1, node2, weight=weight)

        # Print path
        print(strongest_path.edges())
        # Save graph
        filename = "{0}.cluster_{1}.gexf".format(args.clusters, i)
        networkx.write_gexf(strongest_path, filename)

        # Clean up (?)
        del g
        del strongest_path




##########################

if __name__ == '__main__':
    main()
