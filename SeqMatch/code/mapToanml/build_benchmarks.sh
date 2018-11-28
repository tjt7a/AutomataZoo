#!/bin/bash
DATA=../GSP_CPU/intermidiate-size6.txt

# build anml
#python py_spm_real.py -s 6 -p ${DATA} --NC
#python py_spm_real.py -s 10 -p ${DATA} --NC
python py_spm_real.py -s 6 -p ${DATA}
python py_spm_real.py -s 10 -p ${DATA}

