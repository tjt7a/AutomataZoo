#!/usr/bin/python
#
# by Jack Wadden
#

import random
import sys

def usage():
    sys.stdout.write("USAGE: python name_generator.py <num_db_names> <num_input_names> <seed>\n")

def induce_error(in_string):
    # Induce errors in non delimiter chars
    alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    # pick an index to induce the error
    index = random.randint(0, len(in_string) - 1)
    # induce the error
    retval = in_string[:index] + random.choice(alpha) + in_string[index + 1:]
    return retval


#######################################################3

if len(sys.argv) < 4:
    usage()
    sys.exit(1)

# Parse args
num_db_names = int(sys.argv[1])
num_input_names = int(sys.argv[2])
seed = int(sys.argv[3])

# hard coded probabilities for input
shorten_prob = 0.05
roman_prob = 0.05
nickname_prob = 0.05
error_prob = 0.05
name_occur = 0.01

# hard coded name files
first_male_fn = '../data/dist.male.first'
first_female_fn = '../data/dist.female.first'
last_fn = '../data/dist.all.last'

# Seed prng
random.seed(seed)

# Open first and last name files
first_male_lines = []
with open(first_male_fn) as first_file:
    first_male_lines = first_file.readlines()

first_female_lines = []
with open(first_female_fn) as first_file:
    first_female_lines = first_file.readlines()

last_names_lines = []
with open(last_fn) as last_file:
    last_names_lines = last_file.readlines()

# Sanitize input SAA names JACK -> Jack
male_first_names = []
for line in first_male_lines:
    name = line.split(' ')[0]
    name = name[0] + name[1:].lower()
    male_first_names.append(name)

female_first_names = []
for line in first_female_lines:
    name = line.split(' ')[0]
    name = name[0] + name[1:].lower()
    female_first_names.append(name)

first_names = male_first_names + female_first_names

last_names = []
for line in last_names_lines:
    name = line.split(' ')[0]
    name = name[0] + name[1:].lower()
    last_names.append(name)


# Generate database names
db_names = []
db_names_string = ""
for i in range(0,num_db_names):

    name = []

    # get a random first name
    first_index = random.randint(0,len(first_names)-1)
    first_name = first_names[first_index].strip()

    # get a random last name
    last_index = random.randint(0,len(last_names)-1)
    last_name = last_names[last_index].strip()

    name.append(last_name)
    name.append(first_name)

    db_names.append(name)
    db_names_string = db_names_string + last_name + ", " + first_name + "\n"

# Generate input names
input_names = "$"
for i in range(0, num_input_names):

    # either get a random name, or get a db name
    if random.random() < name_occur :
        # database name
        entry = random.randint(0, len(db_names) - 1)
        last_name = db_names[entry][0]
        first_name = db_names[entry][1]
    else:
        # random name
        last_name = last_names[random.randint(0,len(last_names)-1)]
        first_name = first_names[random.randint(0,len(first_names)-1)]

    # should we add an error?
    if random.random() < error_prob:
        if random.random() < .5 :
            first_name = induce_error(first_name)
        else:
            last_name = induce_error(last_name)

    # do we shorten Jack to J.?
    if random.random() < shorten_prob:
        first_name = first_name[0] + "."

    # do we add a nickname?
    nickname = ""
    if random.random() < nickname_prob:
        nickname = " (" + first_names[random.randint(0,len(first_names)-1)] + ")"

    # does the name have roman numerals?
    roman_nums = ""
    if random.random() < roman_prob :
        roman_nums = " " + random.choice(["II","III","IV","V"]);

    delimiter = "$"
    whole_name = last_name + roman_nums + ", " + first_name + nickname + delimiter

    input_names = input_names + whole_name


# Write DB out to file
db_fn = sys.argv[1] + "_names.db"
inputs_fn = sys.argv[2] + "_names.input"

with open(db_fn, "w") as text_file:
        text_file.write(db_names_string)

with open(inputs_fn, "w") as text_file:
        text_file.write(input_names)
