#!/usr/bin/python
import sys
import random


def usage():
    print "USAGE: genDNAseqs.py <seed> <num_seqs> <length>"

#
if len(sys.argv) != 4 :
    usage()
    sys.exit(1)

seed = int(sys.argv[1])
random.seed(seed)
num_seqs = int(sys.argv[2])
length = int(sys.argv[3])

for i in range(0,num_seqs):
    for j in range(0,length):
        sys.stdout.write(random.choice(['a','t','g','c']))

    sys.stdout.write("\n")

