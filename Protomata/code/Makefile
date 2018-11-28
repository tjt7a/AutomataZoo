CC=g++
FLAGS=-std=c++11 -O3
IHS=/if10/jpw8bd/r/automata/regex_comparison/engines/hyperscan/src
LHS=/if10/jpw8bd/r/automata/regex_comparison/engines/hyperscan/build/lib
LIB=-lhs

all:
	${CC} ${FLAGS} main.cpp -I${IHS} -L${LHS} ${LIB} -o ps_scan_hyperscan
