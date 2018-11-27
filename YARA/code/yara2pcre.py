#
#  Converts yara rules to PCRE
#
import os
import sys
import plyara
import re
import string

#
def addDelimiters(string):
    delim = "/"
    return delim + string + delim

# Converts list of 0-255 int values to a string charset
def values2Charset(values):
    retval = "["
    for val in values:
        #
        retval = retval + "\\x" + hex(val)[2:]
    return retval + "]"

# Converts two string hex chars to a charset. ? indicates a nibble wildcard
def nibbles2Charset(high, low):
    result = ""
    values = list()
    if high == '?':
        if low == '?':
            result = '.'
        else:
            # find charset where high nib can be anything
            low_val = int(low, 16)
            for i in range(0,255):
                # mask low bits and compare
                if (i & 15) == low_val:
                    values.append(i)

            result = values2Charset(values)
    else:
        if low == '?':
            # find charset where high nib can be anything
            high_val = int(high, 16)
            for i in range(0,255):
                # mask low bits and compare
                if (i >> 4 & 15) == high_val:
                    values.append(i)

            result = values2Charset(values)
        else:
            result = "\\x" + high + low

    return result

# Converts a YARA hex string to a regular expression
def hexStringToRegex(hex_string):
    print "HEX TO REGEX START"
    done = False
    counter = 0
    result = ""
    states = ['normal','jump','alternative']
    state = 'normal'
    index = 0
    while not done :
        # loop over characters
        #get next byte
        char = hex_string[index]
        index = index + 1
        # ignore these chars
        if char == ' ':
            continue
        elif char == '\n':
            continue
        elif char == '{':
            continue
        # include these chars
        elif char == '(':
            result = result + char
            continue
        elif char == ')':
            result = result + char
            continue
        elif char == '|':
            result = result + char
            continue
        # end condition
        elif char == '}':
            done = True
        # jump handling
        elif char == '[':
            state = 'jump'
            continue
        elif char == ']':
            state = 'normal'
            continue
        # others
        else:
            # ignore jumps for now
            if state == 'jump':
                continue
            # we need to handle a byte pattern
            else:
                counter = counter + 1
                if counter == 2:
                    charset = nibbles2Charset(hex_string[index - 2], char)
                    result = result + charset
                    counter = 0

    print result
    print "HEX TO REGEX END"
    return result

# Parses a YAR file and emits regular expressions to a file
def parseYARFile(file_path, file_name):
    sys.stdout.write("  - parsing input file: " + file_path + "\n")
    # read input file
    p = plyara.PlyaraParser()
    try:
        result = p.parseFromFile(file_path)
    except:
        sys.stdout.write("PARSER BARFED: " + file_path + "\n")
        return

    rules = ""
    wide_rules = ""

    rule_counter = 0
    string_counter = 0
    for rule in result:
        rule_name = rule['rule_name']
        #sys.stdout.write("FOUND RULE: " + rule_name + "\n")
        rule_counter = rule_counter + 1
        if 'strings' in rule:
            for strings in rule['strings']:
                print strings
                string_counter = string_counter + 1
                id_string =  file_name + "." + rule_name + "." + strings['name']
                #sys.stdout.write(id_string + " : " + strings['value'] + "\n")
                final_rule = strings['value']

                if final_rule.startswith("{"):
                    final_rule =  hexStringToRegex(final_rule)
                    final_rule = addDelimiters(final_rule)
                elif final_rule.startswith("\""):
                    # NEED TO ESCAPE SPECIAL CHARS HERE TO CONVERT TO EXACT MATCH STRING
                    # TODO
                    final_rule = final_rule[1:-1]
                    escaped = final_rule.replace("\\", "\\\\")
                    escaped = escaped.replace(".", "\.")
                    escaped = escaped.replace("^", "\^")
                    escaped = escaped.replace("|", "\|")
                    escaped = escaped.replace("$", "\$")
                    escaped = escaped.replace("*", "\*")
                    escaped = escaped.replace("+", "\+")
                    escaped = escaped.replace("?", "\?")
                    escaped = escaped.replace("(", "\(")
                    escaped = escaped.replace(")", "\)")
                    escaped = escaped.replace("[", "\[")
                    escaped = escaped.replace("]", "\]")
                    escaped = escaped.replace("{", "\{")
                    escaped = escaped.replace("}", "\}")
                    final_rule = addDelimiters(escaped)
                else:
                    # this is actually a regex already =P
                    print "FOUND_REGEX"
                    final_rule = final_rule

                # Now that we have a regex, check for modifiers
                ascii = False
                fullword = False
                wide = False
                nocase = False
                orig_rule = final_rule
                if 'modifiers' in strings :

                    for mod in strings['modifiers']:
                        if mod == 'ascii':
                            # basically ignored unless also will wide mod
                            ascii = True
                            continue
                        elif mod == 'fullword':
                            # can only match if delimited by non-alphanumeric chars
                            # [^0-9a-zA-Z]<pattern>[^0-9a-zA-Z]
                            fullword = True
                            final_rule = "/[^0-9a-zA-Z]" + final_rule[1:]
                            if nocase:
                                final_rule = final_rule[:-2] + "[^0-9a-zA-Z]/i"
                            else:
                                final_rule = final_rule[:-1] + "[^0-9a-zA-Z]/"
                            continue
                        elif mod == 'wide':
                            # interleave ascii pattern with zeroes
                            # BEFORE: pattern
                            # AFTER: p\x00a\x00t\x00t\x00e\x00r\x00n\x00
                            wide = True
                            continue
                            # each byte actually needs to be two bytes
                        elif mod == 'nocase':
                            # add pcre modifier 'i' case insensitive to pcre
                            final_rule = final_rule + "i"
                            nocase = True
                            continue
                        else:
                            #do nothing
                            continue

                #
                # add original ascii rule as well as wide rule
                if wide:
                    #wide_rules = wide_rules + id_string + " : " + final_rule + "\n"
                    wide_rules = wide_rules + final_rule + "\n"
                    if ascii:
                        #rules = rules + id_string + " : " + final_rule + "\n"
                        rules = rules + final_rule + "\n"
                else:
                    #rules = rules + id_string + " : " + final_rule + "\n"
                    rules = rules + final_rule + "\n"

    return rules,wide_rules

def main():
    sys.stdout.write("*******************************\n");
    sys.stdout.write("YARA2PCRE by Jack Wadden\n")
    sys.stdout.write("*******************************\n");


    # change directory to base yara rule dir
    #input_rule_dir = sys.argv[1]
    rules_dir = "/af5/jpw8bd/r/automata/YARA/rules"

    rules = ""
    wide_rules = ""

    for root, subdirs, files in os.walk(rules_dir):
        for name in files:
            if name.endswith(".yar"):
                if "index" not in name:
                    if "utils" not in root:
                        fn = os.path.join(root, name)
                        #print(fn)
                        new_rules = parseYARFile(fn, name)
                        if new_rules is not None:
                            if new_rules[0] is not None:
                                rules = rules + new_rules[0]
                                if new_rules[1] is not None:
                                    wide_rules = wide_rules + new_rules[1]

    # write rules to file
    with open("YARA_rules.txt", "w") as text_file:
            text_file.write(rules)
    with open("YARA_wide_rules.txt", "w") as text_file:
            text_file.write(wide_rules)

if __name__== "__main__":
    main()
