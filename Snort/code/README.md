# Snort NIDS Ruleset

# 
1. Download snort rules into rules/
2. Use extract_pcre.py to pull out all PCRE rules from snort rules
3. Use hscompile to identify which rules can be compiled by Hyperscan
4. Filter these rules used filter_mods.py to ignore rules where there are Snort specific modifiers
5. Resulting rules are the Snort benchmark


# Input generation
1. Looked at PCAPs from this site: https://archive.wrccdc.org/pcaps
2. Picked this PCAP file https://archive.wrccdc.org/pcaps/2012/wrccdc2012.pcap.gz
