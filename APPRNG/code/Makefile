CC=g++-5
FLAGS=-O3 --std=c++11 -pthread -DDEBUG=false -g
VASIM=$(HOME)/r/automata/AutomataZoo/AZ2_stats/VASim
MNRL=$(VASIM)/libs/MNRL/C++
LIBMNRL=$(MNRL)/libmnrl.a
PUGI=$(VASIM)/libs/pugixml/src
LIBVASIM=$(VASIM)/libvasim.a
IDIRS=-I $(VASIM)/include -I $(MNRL)/include -I $(PUGI)
TARGET=apprng

all:
	$(CC) $(IDIRS) $(FLAGS) main.cpp $(LIBVASIM) $(LIBMNRL) -o $(TARGET)

