# Hamming

# How was I made?
1. Used ham program in code directory to generate hamming automata of different sizes
2. Picked ed=3,5,10 as good benchmark hamming distances.
3. Used profiling to decide length. Looked for a length where average reports are 1/1,000,000 inputs.
4. Generated 1,000 widgets of these {hd,length} combinations to form each benchmark.

# Hamming Distance Automata Generators

/ham contains a program that reads sequences from lines in files and then generates hamming distance filters according to an input distance.

/patterns contains the pattern files, generator code, and documentation for how to build the pattern files used to generate the Hamming benchmarks.
