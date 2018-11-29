# AutomataZoo Automata Processing Benchmark Suite

AutomataZoo is an automata processing benchmark suite and is an improved version of [ANMLZoo](https://github.com/jackwadden/ANMLZoo)

If you have any questions or comments, please contact tjt7a@virginia.edu or create an Issue Ticket.

## Description

High performance automata-processing engines are traditionally evaluated by computing a limited set of regular expression rulesets. These serve as valid, real-World example use cases, but they only represent a small proportion of all automata-based applications. With the recent availability of architectures and software frameworks for automata processing, many new applications have been discovered that benefit from automata processing. These demonstrate a broad variety of characteristics that differ from prior regular expression-based applications, and warrant their own benchmarks.

## Improvements over ANMLZoo

AutomataZoo improves upon ANMLZoo in several ways:

- The suite of benchmarks is not standardized to a particular architecture, and does not inherit the same architectural biases as ANMLZoo.

- The benchmarks implement full kernels, which allows for comparisons between automata and non-automata approaches.

- The suite includes open-source tools for generating benchmark automata and inputs of various sizes, allowing for design space explorations.


## Benchmarks

1. **Snort:** A widely used network intrusion detection system.
2. **ClamAV:** A virus-detection tool that relies on a publicly-available database of malware patterns.
3. **Protomata:** An automata-based application that searches for a set of 1309 protein motif patterns from the PROSITE database.
4. **Brill Tagging:** A rule-based approach to part-of-speech tagging.
5. **Random Forest:** A machine learning model based on ensembles of decision trees.
6. **Hamming Distance:** A string scoring kernel that measures the number of mutations between two strings.
7. **Levenshtein Distance:** A string scoring kernel that measures the number of edits between two strings.
8. **Sequence Matching:** An automata application that counts sorted sequences of item sets to identify frequently-occurring sets.
9. **Entity Resolution:** An automata application that attempts to find duplicate entries in a streaming database.
10. **CRISPR/Cas9:** An automata application that enabled gene editing by identifying targetted locations.
11. **YARA:** An automata application that discovers malware described in the YARA malware pattern description language.
12. **File Carving:** An automata application that identifies files in a stream of input bytes.
13. **Pseudo Random Number Generation (PRNG):** An automata application that models Markov Chains with finite automata to generate a high-throughput PRNG streams.


## Benchmark Contributors

Jack Wadden<br>
Tommy Tracy II<br>
Elaheh Sadredini<br>
Lingzi Wu<br>
Chunkun Bo<br>
Jesse Du<br>
Yizhou Wei<br>
Matthew Wallace<br>
Jeffrey Udall<br>
Vinh Dang<br>
Deyuan Guo<br>
Ke Wang<br>
Nathan Brunelle<br>
Matt Grimm<br>

If you use this benchmark suite in a publication, please use the following citation:

Wadden, J., Tracy II, T., Sadredini, E., Wu, L., Bo, C., Du, J., Wei, Y., Wallace, M., Udall, J., Stan, M., and Skadron, K. "ANMLZoo: A Benchmark Suite for Exploring Bottlenecks in Automata Processing Engines and Architectures." 2016 IEEE International Symposium on Workload Characterization (IISWC'18). IEEE, 2018.

```
@inproceedings{ANMLZoo,  
    title={{ AutomataZoo: A Modern Automata Processing Benchmark Suite}},  
    author={Wadden, Jack and Tracy II, Tom and Sadredini, Elaheh and Wu, Lingzi and Bo, Chunkun and Du, Jesse and Wei, Yizhou and Wallace, Matthew and Udall, Jeffrey and Stan, Mircea and Skadron, Kevin},
    booktitle={Proceedings of the IEEE International Symposium on Workload Characterization (IISWC)},  
    year={2018},  
}
```

## License
Each benchmark and automata processing engine in AutomataZoo is individually licensed. Please refer to the benchmark directories for individual license files.