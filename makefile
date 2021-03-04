CXX=g++
CXXFLAGS=-Wall -Wextra -pedantic -Werror -std=c++17 -O3 -g
LDFLAGS=$(CXXFLAGS)
OBJ=$(SRC:.cc=.o)
BUILDDIR=out/

all: demo

%.o: %.cc
	$(CXX) $(CXXFLAGS) $(OPTFLAGS) -c $< -o $@

clean:
	rm *.o
	rm *.bin

demo: thc.o
	$(CXX) $(LDFLAGS) demo.cc -o $@ $^