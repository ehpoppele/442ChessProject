import pexpect
import time


if __name__ == "__main__":
    stockfish = pexpect.spawn("./stockfish")
    stockfish.expect('')
    stockfish.sendline("setoption name Threads value 24 position fen 8/8/8/8/8/6k1/5q2/7K w - - 0 1")
    stockfish.expect('')
    start = time.perf_counter()
    stockfish.sendline("go btime 50000")
    stockfish.expect("bestmove .*")
    elapsed = time.perf_counter() - start
    print(elapsed)
    bytes = stockfish.after
    bytes2 = stockfish.before
    string = bytes.decode('utf-8')
    string2 = bytes2.decode('utf-8')
    print(string)
    print(string2)
    move = string.split()[1]
    print(move)
