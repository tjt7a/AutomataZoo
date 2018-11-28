# Protomata

# How was I made?
1. Get prosite.dat signature file
2. Run dupe_prosite.py file using the args "1309 prosite.dat 1309.dat" to extract patterns into new file.
3. Use PS Scan code written by Matt Grimm to extract regular expressions.
4. Repeat 3 with "skip common" enabled. This ignores patterns that match frequently.
5. Use pcre2mnrl to convert two regular expression files to two automata graphs.
