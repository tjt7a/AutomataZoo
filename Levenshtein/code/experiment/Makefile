CC=g++-5
FLAGS=-O3 --std=c++11 -pthread -DDEBUG=false -g
VASIM=$(HOME)/r/automata/VASim
MNRL=$(VASIM)/libs/MNRL/C++
LIBMNRL=$(MNRL)/libmnrl.a
PUGI=$(VASIM)/libs/pugixml/src
LIBVASIM=$(VASIM)/libvasim.a
IDIRS=-I $(VASIM)/include -I $(MNRL)/include -I $(PUGI) -I../lev
TARGET=lev_search

all:
	$(CC) $(IDIRS) $(FLAGS) lev_search.cpp ../lev/lev.o $(LIBVASIM) $(LIBMNRL) $< -o lev_search

