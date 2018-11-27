# A tool for converting ClamAV virus signatures to PCRE regex.
# (c) University of Virginia. All rights reserved.
# Author: Deyuan Guo <dg7vp@virginia.edu>
#         Jack Waden <jackwadden@gmail.com>
# Date: Apr 12, 2016
#       March 30, 2018

from curses.ascii import *
import sys

# PCRE: Convert hex values to PCRE
# Examples: 'aa' -> '\xaa', '??' -> '.', '?a' -> '(\x0a|\x1a|\x2a|...)'
def hex_to_pcre(s):
    assert(len(s) % 2 == 0)
    pcre = ''
    for i in range(0, len(s), 2):
        t = s[i:i+2]
        if t[0] == '?' and t[1] == '?': # '??'
            pcre = '.'
        elif t[0] == '?': # '?a'
            pcre += '('
            lo = int(t[1], 16)
            for i in range(16):
                pcre += ('\\x%02x' % (i * 16 + lo)) + '|'
            pcre = pcre[:-1] + ')'
        elif t[1] == '?': # 'a?'
            pcre += '('
            hi = int(t[0], 16)
            for i in range(hi * 16, hi * 16 + 16):
                pcre += ('\\x%02x' % i) + '|'
            pcre = pcre[:-1] + ')'
        else: # 'aa'
            pcre = '\\x' + t
    return pcre

# Get current RegEx type
def get_type(sig, i):
    if i >= len(sig):
        return 'eol'
    elif isxdigit(sig[i]) or sig[i] == '?':
        if i+1 < len(sig) and (isxdigit(sig[i+1]) or sig[i+1] == '?'):
            return 'hex'
        else:
            return 'halfhex'
    elif sig[i] == '*':
        return 'star'
    elif sig[i] == '(':
        j = i + 1;
        while isxdigit(sig[j]) and isxdigit(sig[j+1]) and sig[j+2] == '|':
            j += 3
        if isxdigit(sig[j]) and isxdigit(sig[j+1]) and sig[j+2] == ')':
            return 'byteor'
        else:
            return 'stror'
    elif sig[i] == '{':
        j = i + 1;
        range = False
        while sig[j] != '}':
            if sig[j] == '-':
                range = True
            j += 1
        if sig[i+1] == '-':
            return 'less'
        elif sig[j-1] == '-':
            return 'more'
        elif range:
            return 'range'
        else:
            return 'exact'
    elif sig[i] == '[':
        return 'anchor'
    else:
        return 'unknown'

# Determine the end of current regex component
def idx_of_next(str, i, c):
    j = i + 1
    while j < len(str) and str[j] != c:
        j += 1
    return j

# Convert a line of signature to PCRE
def sig_to_pcre(sig):
    quantifier = 0
    large_quantifier = 0
    sig_pcre = ''
    i = 0
    while i <= len(sig):
        type = get_type(sig, i)
        if type == 'eol':
            break
        elif type == 'hex': # aaa??a??
            sig_pcre += hex_to_pcre(sig[i:i+2])
            i += 2
        elif type == 'star': # *
            sig_pcre += '.*'
            i += 1
        elif type == 'byteor' or type == 'stror': # (aa|bb|ccdd|..)
            sig_pcre += '('
            j = idx_of_next(sig, i, ')')
            sym = sig[i+1:j]
            syms = sym.split('|')
            for k in range(len(syms)):
                sig_pcre += hex_to_pcre(syms[k])
                sig_pcre += '|'
            sig_pcre += ')'
            i = j + 1
        elif type == 'more': # {n-}
            j = idx_of_next(sig, i, '}')
            target = sig[i+1:j-1]
            quantifier = 1
            if int(target) > 2047:
                large_quantifier = 1
            sig_pcre += '.{' + target + ',}'
            i = j + 1
        elif type == 'less': # {-n}
            j = idx_of_next(sig, i, '}')
            target = sig[i+2:j]
            quantifier = 1
            if int(target) > 2047:
                large_quantifier = 1
            sig_pcre += '.{,' + target + '}'
            i = j + 1
        elif type == 'range': # {m-n}
            j = idx_of_next(sig, i, '}')
            target = sig[i+1:j].split('-')
            quantifier = 1
            if int(target[1]) > 2047:
                large_quantifier = 1
            sig_pcre += '.{' + target[0] + ',' + target[1] + '}'
            i = j + 1
        elif type == 'exact': # {n}
            j = idx_of_next(sig, i, '}')
            target = sig[i+1:j]
            quantifier = 1
            if int(target) > 2047:
                large_quantifier = 1
            sig_pcre += '.{' + target + '}'
            i = j + 1
        elif type == 'anchor':
            target = sig[i+1:j].split('-')
            sig_pcre += '.{' + target[0] + ',' + target[1] + '}'
            i = j + 1
        else:
            print 'Unsupported signature:', sig
            print 'Ignoring...'
            return None

    global quantifier_cnt
    quantifier_cnt += quantifier
    global large_quantifier_cnt
    large_quantifier_cnt += large_quantifier
    return sig_pcre


# Entry
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python sig_to_pcre.py <sig_file.sigs>'
        sys.exit(0)

    # Config
    sigfile = sys.argv[1]
    sigfile_name = sys.argv[1][0:sys.argv[1].rfind('.sigs')]
    outfile = sigfile_name + '.pcre'

    # Input sigs

    print 'Converting', sigfile, 'to PCRE...'
    with open(sigfile) as f:
        sigs = f.read().splitlines()
    print len(sigs), 'lines in', sigfile

    # Output file
    out = open(outfile, 'w+')

    quantifier_cnt = 0
    large_quantifier_cnt = 0

    for sig in sigs:
        if len(sig) != 0:
            #sys.stdout.write(".")
            #sys.stdout.flush()
            pcre = sig_to_pcre(sig)
            if pcre is not None:
                out.write('/')
                out.write(pcre)
                out.write('/\n')
    print 'Done! '
    print 'Wrote all pcres to',outfile
    print '  There are ' + str(quantifier_cnt) + ' regexes with quantifiers.'
    print '  There are ' + str(large_quantifier_cnt) + ' regexes with quantifiers >= 2048.'
