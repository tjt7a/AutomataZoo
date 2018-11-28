# SEQ MATCH

# How was automata built?

## Build candidate sets
1. Use gsp_cpu using frequency 0.02 and BIBLE.txt and dump intermediate data sets.
2. Choose 6 size sets for experiments

## Build map file
1. ./inputMapping 0.02 BIBLE.txt
2. This generates map.txt and seq.txt

## Build ANML
1. Move seq.txt and map.txt to same directory as py_spm_real
3. Use py_spm_real.py to generate ANML
4. python py_spm_real.py -s 6 -p intermediate-size6.txt
8. Flatten each using flattener:
9. python flattener.py 

# How was input built?
