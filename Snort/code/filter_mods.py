#
# This script takes all regular expressions successfully compileable by hyperscan
#  and filters out all rules with Snort specific modifiers.
#
import sys

def extract_mods(line):
    retval = ""
    mod_start = line.rfind("/")
    if mod_start != len(line) - 2:
        mods = line[mod_start + 1 :len(line)]
        retval = mods

    return retval

######################################
# all modifiers we're trying to filter
snort_mods = {'P','U','R','I','H','D','M','C','K','S','Y','B','O'}
counter = 0
clean_counter = 0
pcre_counter = 0
U_counter = 0
R_counter = 0
P_counter = 0
I_counter = 0
H_counter = 0
D_counter = 0
M_counter = 0
C_counter = 0
K_counter = 0
S_counter = 0
Y_counter = 0
B_counter = 0
O_counter = 0
G_counter = 0
E_counter = 0

if len(sys.argv) != 2:
    print "USAGE: python filter_mods.py <input_regex>"
    sys.exit(1)

infile_fn = sys.argv[1]

with open(infile_fn) as f:
    for line in f:
        counter = counter + 1


        mods = extract_mods(line)
        pcre_only = True

        if len(mods) > 0:
            if mods.find("P") >= 0:
                P_counter = P_counter + 1
                pcre_only = False
            if mods.find("U") >= 0:
                U_counter = U_counter + 1
                pcre_only = False
            if mods.find("R") >= 0:
                R_counter = R_counter + 1
                pcre_only = False
            if mods.find("I") >= 0:
                I_counter = I_counter + 1
                pcre_only = False
            if mods.find("H") >= 0:
                H_counter = H_counter + 1
                pcre_only = False
            if mods.find("D") >= 0:
                D_counter = D_counter + 1
                pcre_only = False
            if mods.find("M") >= 0:
                M_counter = M_counter + 1
                pcre_only = False
            if mods.find("C") >= 0:
                C_counter = C_counter + 1
                pcre_only = False
            if mods.find("K") >= 0:
                K_counter = K_counter + 1
                pcre_only = False
            if mods.find("S") >= 0:
                S_counter = S_counter + 1
                pcre_only = False
            if mods.find("Y") >= 0:
                Y_counter = Y_counter + 1
                pcre_only = False
            if mods.find("B") >= 0:
                B_counter = B_counter + 1
                pcre_only = False
            if mods.find("O") >= 0:
                O_counter = O_counter + 1
                pcre_only = False
            if mods.find("G") >= 0:
                G_counter = G_counter + 1
                pcre_only = False
            if mods.find("E") >= 0:
                E_counter = E_counter + 1
                pcre_only = False

            if pcre_only:
                pcre_counter = pcre_counter + 1
                sys.stdout.write(line)
        else:
            clean_counter = clean_counter + 1
            sys.stdout.write(line)

'''
print "Total:",counter
print "Clean:",clean_counter
print "PCRE:",pcre_counter
print "P:",P_counter
print "U:",U_counter
print "R:",R_counter
print "I:",I_counter
print "H:",H_counter
print "D:",D_counter
print "M:",M_counter
print "C:",C_counter
print "K:",K_counter
print "S:",S_counter
print "Y:",Y_counter
print "B:",B_counter
print "O:",O_counter
print "G:",G_counter
print "E:",E_counter
'''
