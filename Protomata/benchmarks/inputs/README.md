# How was I generated?
1. Download human proteome using the link in the license. When downloaded for standard input generation, the database was over 230MB.
2. sanitize_fasta.py in the scripts directory enables you to choose sequential signatures from this database for inclusion in an input file.
3. The standard input was generated using the following command: python proteome_sanitizer.py <entire_human_proteome>.fasta 0 30000 > 30k_prots.input
