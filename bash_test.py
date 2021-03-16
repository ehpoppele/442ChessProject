import pexpect
import time


if __name__ == "__main__":
    stockfish = pexpect.spawn("./stockfish")
    stockfish.expect('')
    stockfish.sendline("setoption name Threads value 24 position fen r1bqkb1r/pppp1ppp/2n2n2/4p1N1/2B1P3/8/PPPP1PPP/RNBQK2R b KQkq - 5 4")
    stockfish.expect('')
    start = time.perf_counter()
    stockfish.sendline("go btime 50000")
    stockfish.expect("bestmove .*")
    elapsed = time.perf_counter() - start
    print(elapsed)
    bytes = stockfish.after
    string = bytes.decode('utf-8')
    print(string)
    move = string.split()[1]
    print(move)
