import pexpect
import time

def launchEngine(name, threads):
    engine = pexpect.spawn("./" + name)
    engine.expect('')
    engine.sendline("setoption name Threads value 24")
    engine.expect('')
    return engine


def getMove(engine, fen, black_time, white_time):
    engine.sendline("position fen " + fen)
    engine.expect('')
    start = time.perf_counter()
    engine.sendline("go btime " + str(black_time) + " wtime " + str(white_time))
    engine.expect("bestmove .*")
    elapsed = time.perf_counter()-start
    bytes = engine.after
    string = bytes.decode('utf-8')
    move = string.split()[1]
    return(move, elapsed)

