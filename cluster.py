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
