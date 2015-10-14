# 10x_scripts

Got a .bam file containing barcoded reads aligned to a reference genome? Good for you!

First get a sparse matrix using `sparse_matrixer.py`:

`samtools view foo.bam | python sparse_matrixer.py > my_sparse_matrix.tsv`

Then use that sparse matrix to form clusters with `clusterer.py`:

`python clusterer.py --sparse-matrix my_sparse_matrix.tsv --number-of-clusters <number>`

Coming soon ... order the contigs in your cluster using `orderer.py`!
