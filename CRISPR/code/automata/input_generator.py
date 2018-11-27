#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

@author: bochunkun
"""

import sys
import random


if len(sys.argv) != 4:
    print "USAGE: python input_generator.py <num_patterns> <pam> <seed>"
    sys.exit(1)

number = int(sys.argv[1])
pam = sys.argv[2]
seed = int(sys.argv[3])
random.seed(seed)

foo = ['A','T','G','C']
for i in range(number):
    for j in range(20):
        sys.stdout.write(random.choice(foo)),
    print pam
#print ''
