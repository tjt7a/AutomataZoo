# CRISPR Input Generation

All inputs are just DNA sequences. We use the first 10MB of Chromosome 1 of the Human genom with ambiguous base pairs stripped. You can generate this input by running the following commands:

``` bash
wget http://hgdownload.cse.ucsc.edu/goldenPath/hg38/chromosomes/chr1.fa.gz
gunzip chr1.fa.gz
python extract_dna.py 10000000 chr1.fa > 10MB
```
