import pexpect
import time

def launchEngine(name, threads):
    engine = pexpect.spawn("./" + name)
    engine.expect('')
    engine.sendline("setoption name Threads value " + str(threads))
    engine.expect('')
    engine.sendline("position startposition")
    engine.expect('')
    return engine


def getMove(engine, fen, black_time, white_time):
    if fen == 'draw':
        return ('draw', 0)
    engine.sendline("position fen " + fen)
    engine.expect('')
    start = time.perf_counter()
    engine.sendline("go btime " + str(black_time) + " wtime " + str(white_time))
    engine.expect("bestmove .*")
    elapsed = time.perf_counter()-start
    bytes = engine.after
    string = bytes.decode('utf-8')
    move = string.split()[1]
    if move == "(None)":
        #If None was returned, the game is over. We check whether it was draw or mate
        #stockfish gives '... cp 0' for draw and '... mate 0' for mate on the last line
        #so we only check for p or e as the 3rd to last char
        end_string = engine.before.decode('utf-8')
        end_char = end_string[len(end_string)-3]
        if end_char == 'p':
            move = 'draw'
        elif end_char == 'e':
            move = 'loss_mate'
        else:
            print("Game has ended with unrecognized return")
            assert False
    return(move, elapsed*1000) #multiply to get millisecond

