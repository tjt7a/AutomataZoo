# Copyright (c) Micron Technology, Inc. All rights reserved.
#
# Levenshtein makefile

all: approx_string_match

approx_string_match:  approx_string_match.c
	gcc $(EXTRA_CFLAGS) -g -o $@ $< -lapexec -lapcompile 

clean:
	rm -f *.o approx_string_match

### Commented out during release builds
#include Makefile.devel
