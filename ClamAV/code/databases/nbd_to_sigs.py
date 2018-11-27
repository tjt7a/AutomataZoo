# Deyuan Guo, Feb 2015
# Jack Wadden, March 2018

# extract signatures from *.ndb or *.ndu

import sys

if len(sys.argv) != 2:
    print 'Usage: python extract_ndb.py <ndb_file.ndb>'
    sys.exit(0)

end_index = sys.argv[1].rfind(".ndb")
database_name = sys.argv[1][0:end_index]

print 'Extracting virus signatures from', sys.argv[1]

# Read database
with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

# Parse database
counter = 0
sigs = ""
for l in lines:
    k = l.split(':')

    # Look for sigs applied to any file
    if k[1] == '0':
        # Look for sigs applied at any offset
        if k[2] == '*':
            counter = counter + 1
            sigs = sigs + k[3] + '\n'

print 'Done! Found',counter,'signatures.'

# Write sigs to new file
sig_file_name = "../sigs/" + database_name + ".sigs"
print "Writing sigs to",sig_file_name
sig_file = open(sig_file_name, "w")
sig_file.write(sigs)
sig_file.close()

# End
