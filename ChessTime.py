import sys
import socket

from TerminalEngine import *
from Board import *

if __name__ == "__main__":
    #Sys args are name of side of player (w/b), engine file, number of threads, port number and maybe more (time control etc?)
    if len(sys.argv) < 5:
        print("Missing an arg")
        assert False
    side = sys.argv[1]
    engine = launchEngine(sys.argv[2], sys.argv[3])
    port = int(sys.argv[4])
    board = Board()
    b_time = 60000
    w_time = 60000
    game_over = False
    listen_socket = None
    game_socket = None
    if side == 'w':
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind(('127.0.0.1', port))#Currently just localhost connection
        listen_socket.listen()
        game_socket, addr = listen_socket.accept()
        print("Connected established by ", addr)
        #make first move
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        my_move, time_used = getMove(engine, fen, b_time, w_time)
        print("My Move: ", my_move)
        w_time -= time_used
        if w_time <= 0:
            print("You fool! You used up all your time on your first move!")
            assert False
        data = bytes(my_move + ' ' + str(time_used), 'utf-8')
        game_socket.sendall(data)
    elif side == 'b':
        game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        game_socket.connect(('127.0.0.1', port))
        print("Connected established to host")
    else:
        print("No valid argument for player side")
        assert False
    while not(game_over):
        data = game_socket.recv(1024)
        opponent_move = data.decode('utf-8').split()[0]
        opponent_time = float(data.decode('utf-8').split()[1])
        print("Opponent Move: ", opponent_move)
        if side == 'w':
            b_time -= opponent_time
            if b_time <= 0:
                if opponent_move != "loss_time":
                    print("Clocks not in agreement!")
                opponent_move = "loss_time"
        else:
            w_time -= opponent_time
            if w_time <= 0:
                if opponent_move != "loss_time":
                    print("Clocks not in agreement!")
                opponent_move = "loss_time"
        if opponent_move == "draw":
            game_over = True
            outcomes.append("draw")
        elif opponent_move == "loss_time":
            game_over = True
            outcomes.append("win_time")
        elif opponent_move == "loss_mate":
            game_over = True
            outcomes.append("win_mate")
        else: #respond with own move
            fen = board.playMove(opponent_move)
            my_move, time_used = getMove(engine, fen, b_time, w_time)
            print("My Move: ", my_move)
            if side == 'w':
                w_time -= time_used
                if w_time <= 0:
                    move = "loss_time"
            else:
                b_time -= time_used
                if b_time <= 0:
                    move = "loss_time"
            if my_move == 'draw':
                game_over = True
                outcomes.append(my_move)
            elif my_move == "loss_time":
                game_over = True
                outcomes.append(my_move)
            elif my_move == "loss_mate":
                game_over = True
                outcomes.append(my_move)
            else:
                fen = board.playMove(my_move)
            print("My Move: ", my_move)
            data = bytes(my_move + ' ' + str(time_used), 'utf-8')
            game_socket.sendall(data)
    game_socket.close()
    if not listen_socket is None:
        listen_socket.close()
    print(outcomes)














