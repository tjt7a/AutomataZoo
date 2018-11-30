# ClamAV

# Construction
1. Download ClamAV database snapshot 0.99.4
2. Download and compile ClamAV 0.99.4 source
3. Use sigtool to extract database from main.cvd "sigtool --unpack-current daily.cvd"
4. Extract all signatures that can be applied to any file at any offset in file in .ndb database using modified version of Deyuan's tool (extract_nbd.py). These signatures have a FileType code (second : separated field) of 0 and an offset code of '*' (https://github.com/Cisco-Talos/clamav-devel/blob/master/docs/signatures.pdf)
5. Use Deyuan's code to convert signatures to PCREs
6. Use pcre2mnrl to convert pcres to mnrl files.


# Input
1. Virus signatures from virus sign
2. Other media files that are creative commons license. See License_Information.txt.
