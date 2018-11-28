#!/usr/bin/python
import sys

def addSlashes(input):
    return "/" + input[:-1] + "/"

with open("protomata_skipcommon.regex") as f:
    lines = f.readlines()
    for line in lines:
        sys.stdout.write(addSlashes(line) + "\n") 
