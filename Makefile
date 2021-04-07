NVCC=/usr/local/cuda/bin/nvcc
DEPENDFLAGS = -std=c++17

SRCS = benchmark.cpp bitbase.cpp bitboard.cpp endgame.cpp evaluate.cpp main.cpp \
	material.cpp misc.cpp movegen.cpp movepick.cpp pawns.cpp position.cpp psqt.cpp \
	search.cpp thread.cpp timeman.cpp tt.cpp uci.cpp ucioption.cpp tune.cpp syzygy/tbprobe.cpp \
	nnue/evaluate_nnue.cpp nnue/features/half_kp.cpp gpu_search.cu

EXE = gpu_stockfish

OBJS = $(notdir $(SRCS:.cpp=.o))

OBJS += gpu_search.o

$(EXE): $(OBJS)
	+$(NVCC) -o $@ $(OBJS)

all: $(EXE) .depend

#%.o: %.cc
#	$(CXX) $(CXXFLAGS) $(OPTFLAGS) -c $< -o $@

clean:
	rm *.o
    
.depend:
	-@$(NVCC) $(DEPENDFLAGS) -MM $(SRCS) > $@ 2> /dev/null

-include .depend