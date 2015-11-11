This is a naive version of the mask, will currently find range where counts are
above a specified threshold.

	python mask_bam.py 20 sample.read_counts.tsv 
	

If you run something like

    python mask_bam.py --maximum-read-count 20 --read-counts-file sample.read_counts.tsv

it should output something like the expected output file.
