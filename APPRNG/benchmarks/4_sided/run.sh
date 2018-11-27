#!/bin/bash
AUTOMATA=automata/apprng_n1000_d4.anml
INPUT=input/10MB_A.prng
INPUT_LEN=${1}

# VASIM FLAGS
FLAGS="-tr"
OPT="-O"


# trim input for evaluation
head -c ${INPUT_LEN} ${INPUT} > ${INPUT}_${INPUT_LEN}.input

vasim ${FLAGS} ${OPT} ${AUTOMATA} ${INPUT}
