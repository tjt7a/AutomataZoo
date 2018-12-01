# Levenshtein

# How was I made?
1. Used lev program in code directory to generate levenshtein of different sizes
2. Picked ed=3,5,10 as good benchmark edit distances.
3. Used profiling to decide length. Looked for a length where average reports are 1/1,000,000 inputs.
4. Generated 1,000 widgets of these {ed,length} combinations to form each benchmark.

