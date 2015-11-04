# Pipeline

- Start out with a `.bam` file with barcoded reads mapped to a reference assembly
- Run `sparse_matrixer.py` to generate a sparse matrix
- Run `clusterer.py` to generate a clusters file from the sparse matrix
- Run `orderer.py` to order the contigs in each cluster
- Run `mirrorer.py` to orient the output a table of orientation info for the ordered contigs

## Example command line

```
# Create a sparse matrix file, only creating connections where each contig
# in question has 20 or more reads from a given barcode, and where the
# common barcode is among the 40 most read-abundant on each contig
samtoools view test.bam | python sparse_matrixer.py --min-reads 20 --head-barcodes 40 >\
test.sparse_matrix
# Now cluster the contigs. Ignore connections between contigs if they have
# fewer than 10 barcodes in common
python clusterer.py --sparse-matrix test.sparse_matrix --minimum-connection-strength 10 >\
test.clusters
# Order the clusters
python orderer.py --sparse-matrix test.sparse_matrix --clusters test.clusters > test.order
# Now orient the ordered contigs
python mirrorer.py # TODO OMG WUT
