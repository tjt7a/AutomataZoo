CC=g++-5
FLAGS=-O3 --std=c++11 -pthread -DDEBUG=false -g
VASIM=$(HOME)/r/automata/VASim
MNRL=$(VASIM)/libs/MNRL/C++
LIBMNRL=$(MNRL)/libmnrl.a
PUGI=$(VASIM)/libs/pugixml/src
LIBVASIM=$(VASIM)/libvasim.a
IDIRS=-I $(VASIM)/include -I $(MNRL)/include -I $(PUGI)
OBJS = util.o zip.o metadata.o main.o jfif.o mpeg.o
TARGET=file_carver

all: $(OBJS)
	$(CC) $(IDIRS) $(FLAGS) $(OBJS) $(LIBVASIM) $(LIBMNRL) -o $(TARGET)

%.o: %.cpp
	$(CC) $(IDIRS) $(FLAGS) -c $<

clean:
	rm *.o
