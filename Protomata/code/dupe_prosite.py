#!/usr/bin/env python
# Written by Matt Grimm (github.com/tkocmathla)

from optparse import OptionParser
import random
import sys

def prosite_patterns(prosite_file, skip_common=True):
    patterns = []
    with open(prosite_file) as fp:
        id = None
        pattern = None
        partial = False
        common = False

        for line in fp:
            line = line.strip()
            if line.startswith('AC '):  # ACcession number
                id = line[5:-1]

            if line.startswith('PA '):  # PAttern line
                if partial:
                    pattern += line[5:]
                else:
                    pattern = line[5:]
                    partial = True
            else:
                partial = False

            if '/SKIP-FLAG=TRUE;' in line:
                common = True

            if pattern and not partial and line == '//':
                if common and skip_common:
                    common = False
                    continue
                pattern = pattern.rstrip('.\n')
                patterns.append([id, pattern])
                pattern = None
    return patterns

def dupe_sigs(max_sigs, input_file, output_file, randomize=False, skip_common=True):
    patterns = prosite_patterns(input_file, skip_common=skip_common)

    with open(output_file, 'w') as f:
        sig_count = 0
        while sig_count < max_sigs:
            for ac, pa in patterns:
                f.write('//\n')
                if sig_count < len(patterns):
                    f.write('ID   {0}; PATTERN.\n'.format(ac))
                    f.write('AC   {0};\n'.format(ac))
                else:
                    f.write('ID   COPY_OF_{0}_{1}; PATTERN.\n'.format(ac, sig_count))
                    f.write('AC   {0}_{1};\n'.format(ac, sig_count))

                # Shuffle the pattern bits for the copies
                if randomize and sig_count > len(patterns):
                    bits = pa.split('-')
                    # Don't move a start anchor bit
                    if pa.startswith('<') or pa.startswith('[<'):
                        bits_tmp = bits[1:]
                        random.shuffle(bits_tmp)
                        bits = [bits[0]] + bits_tmp
                    # Don't move an end anchor bit
                    elif pa.endswith('>') or pa.endswith('>]'):
                        bits_tmp = bits[0:-1]
                        random.shuffle(bits_tmp)
                        bits = bits_tmp + [bits[-1]]
                    else:
                        random.shuffle(bits)
                    pa = '-'.join(bits)

                f.write('PA   {0}.\n'.format(pa))

                sig_count += 1
                if sig_count >= max_sigs:
                    break
        f.write('//\n')

def main():
    usage = 'usage: %prog [options] max_sigs input_file output_file'
    parser = OptionParser(usage)
    parser.add_option('-r', '--randomize', action='store_true', default=False, help='randomize elements of duplicated signatures')
    parser.add_option('-s', '--skip_common', action='store_true', default=False, help='skip common signatures')
    opts, args = parser.parse_args()

    if len(args) < 3:
        parser.error('missing required argument(s)')

    max_sigs, input_file, output_file = args
    dupe_sigs(int(max_sigs), input_file, output_file, randomize=opts.randomize, skip_common=opts.skip_common)

if __name__ == '__main__':
    main()

# vim: nu:et:ts=4:sw=4:fdm=indent
