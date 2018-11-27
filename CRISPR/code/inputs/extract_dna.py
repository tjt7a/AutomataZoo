#!/usr/bin/python

import sys

if len(sys.argv) != 4:
    print "USAGE: ./extract_dna.py <num bps> <infile.fa> <outfile.dna>"
    sys.exit(1)

num_bp = int(sys.argv[1])
fn = sys.argv[2]
outfn = sys.argv[3]

output = ""
counter = 0
with open(fn, "r") as f:
    for line in f:

        # skip the first chr1> line
        if line.strip() == ">chr1":
            continue
        
        # dkip ambiguous bp
        if line.strip() == "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN":
            continue

        output = output + line.strip()

        if len(output) >= num_bp:
            break

#
output = output[:num_bp]

#
with open(outfn, "w") as outfile:
    outfile.write(output)
