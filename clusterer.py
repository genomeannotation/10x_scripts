#!/usr/bin/env python

import sys
import argparse

####################################################################################################

class Clusterer:
    def __init__(self, contig_sim, clusters):
        self.contig_sim = contig_sim
        self.clusters = clusters

    def run(self, desired_clusters):
        while len(self.clusters) > desired_clusters:
            # Find the highest scoring connection between clusters
            highest_score = 0
            best_pair = None
            for i in range(0, len(self.clusters)):
                for j in range(i+1, len(self.clusters)):
                    score = self.compare(self.clusters[i], self.clusters[j])
                    if score > highest_score:
                        highest_score = score
                        best_pair = (i, j)
            # Break if we can't cluster anymore
            if best_pair is None:
                break
            # Remove the clusters
            i = best_pair[0]
            j = best_pair[1]
            cluster_a = self.clusters.pop(max(i, j))
            cluster_b = self.clusters.pop(min(i, j))
            # Merge the clusters
            merged_cluster = cluster_a + cluster_b
            # Add in the merged cluster
            self.clusters.append(merged_cluster)
        print("\n\n".join([str(c) for c in self.clusters]))

    def compare(self, cluster_a, cluster_b):
        score = 0
        for a in cluster_a:
            for b in cluster_b:
                if a in self.contig_sim and b in self.contig_sim[a]:
                    score += self.contig_sim[a][b]
        score /= len(cluster_a)*len(cluster_b)
        return score

####################################################################################################

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
    contig_scores = {} # { contig_a : { contig_b : score } }
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
            if contig_a not in contig_scores:
                contig_scores[contig_a] = {}
            if contig_b not in contig_scores:
                contig_scores[contig_b] = {}
            contig_scores[contig_b][contig_a] = int(barcodes_in_common)
            contig_scores[contig_a][contig_b] = int(barcodes_in_common)

    #####################################
    # Clustering
    #sys.stderr.write("Clustering contigs...\n")
    #clusters = []

    # Initialize every contig as being in its own cluster
    #for contig in contigs:
        #clusters.append([contig])

    #clusterer = Clusterer(contig_scores, clusters)
    #clusterer.run(3)

    #exit()
    
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
