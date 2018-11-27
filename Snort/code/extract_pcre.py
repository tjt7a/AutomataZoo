#!/bin/python

import sys
import glob
import errno
import argparse

parser = argparse.ArgumentParser(description='Extract PCRE regular expressions from Snort rule files.')
parser.add_argument('--rules_path', help='Path to directory holding Snort rules files.', required=True)
parser.add_argument('--regex_fn', help='Path to output file with extracted pcres.', required=True)
args = parser.parse_args()

#path = '/af5/jpw8bd/r/automata/Snort/rules/*.rules'
print args.rules_path
print args.regex_fn

path = str(args.rules_path) + '/*.rules'
regex_fn = str(args.regex_fn)
files = glob.glob(path)

regex_file = open(regex_fn, 'w')

for fn in files:

    f = open(fn, 'r')

    for line in f:
        if "pcre:" in line :
            start = line.find("pcre:")
            end = line.find("\";", start, len(line))

            # we don't support modifiers before the first "
            if line[start+6] != '/':
                sys.stderr.write("Unsupported PCRE: ")
                sys.stderr.write(line[start+6:end])
                sys.stderr.write("\n")
                sys.stderr.write(line[start:end] + "\n")
            else:
                #sys.stdout.write(line[start+6:end] + "\n")
                regex_file.write(line[start+6:end] + "\n")

    f.close()

regex_file.close()
