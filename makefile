CXX=g++
CXXFLAGS= -std=c++17 -O3 -g
LDFLAGS=$(CXXFLAGS)
OBJ=$(SRC:.cc=.o)
BUILDDIR=out/
VPATH=THC/

all: demo

%.o: %.cc %.hh
	$(CXX) $(CXXFLAGS) $(OPTFLAGS) -c -o $@ $<

clean:
	rm *.o
	rm *.bin

demo: thc.o
	$(CXX) $(LDFLAGS) demo.cc -o $@ $^
