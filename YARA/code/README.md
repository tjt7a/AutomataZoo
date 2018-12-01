# YARA Malware Ruleset

# Input source
http://www.tekdefense.com/downloads/malware-samples/Malz.zip

# How was I generated?
1. Downloaded plyara yara rule parser from GitHub: https://github.com/8u1a/plyara. Used commit: c5ea604c147becd74ef3593b9cccd61171948eeb
2. Downloaded YARA rules from GitHub: https://github.com/Yara-Rules/rules. Used commit: 7966196c4002899a0181d8a3366c1c730da43a66.
3. Used yara2pcre.py to parse rules into pcre regular expressions (widened and unwidened versions). This script was built by reading this doc: http://yara.readthedocs.io/en/v3.5.0/writingrules.html
4. Used pcre2mnrl to convert PCREs to automata.
5. Widened automata where appropriate. (vasim --widen)
6. Converted to ANML file format.
7. Looked at rule 24047, 24048, and 12530 due to high reporting
8. These rules are a part of the utils directory and are not included by default. I'm not going to include them in the benchmark.
9. Filtered all yara files from the utils directory and re-built benchmark.
10. 12530 still exists and reports very frequently: /([A-Za-z0-9]{4})*([A-Za-z0-9]{2}==|[A-Za-z0-9]{3}=|[A-Za-z0-9]{4})/
11. Manually removed 12,530 and two other unwidened rules that report frequently out of context (peid.yar.Microsoft_Visual_Cpp_8.$a and peid.yar.Microsoft_Visual_Cpp_8_additional.$a)
12. Manually removed rule 21730 (/......................................................\x8B/) for high reporting.
13. Manually removed rule 21402 (/\x75./) for high reporting.
14. Manually removed 16436 (/.....................\x01/) for high reporting.
15. The motivation for removing these rules is that they are poor filters when applied without context. See section  
15. Rebuilt benchmark.
