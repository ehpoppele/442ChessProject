import subprocess
import time


if __name__ == "__main__":
    stockfish = subprocess.Popen(["./stockfish"])
    outs, errs = stockfish.communicate("setoption name Threads value 24")
    outs, errs = stockfish.communicate("position fen r1bqkb1r/pppp1ppp/2n2n2/4p1N1/2B1P3/8/PPPP1PPP/RNBQK2R b KQkq - 5 4")
    print(errs)
    start = time.perf_counter()
    outs, errs  = stockfish.communicate("go btime 10000")
    elapsed = time.perf_counter() - start
    print(elapsed)
    print(outs)
    print("error ret is:", errs)
