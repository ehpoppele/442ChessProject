import sys
import socket

from TerminalEngine import *
from Board import *

#Defining the data/defaults for each component
bf1_data = {'ip':'192.168.100.2', 'port':4321, 'program':'stockfish_bf1', 'threads':'16', 'wattage':1 }
cpu_data = {'ip':'192.168.100.1', 'port':4321, 'program':'stockfish_cpu', 'threads':'24', 'wattage':1 }
ngd_data = {'ip':'192.168.100.2', 'port':4321, 'wattage':1 } 
sys_data = {'bf1':bf1_data, 'chimera':cpu_data, 'ngd':ngd_data}

#Turns milliseconds into readable clock time
def clockTime(ms):
    h = str(int((ms//1000)//3600))
    m = str(int(((ms//1000)%3600)//60))
    s = str(int((ms//1000)%60))
    f = str(int(ms%1000))
    return (h + ':' + m + ':' + s + '.' + f)

if __name__ == "__main__":
    #Sys args are number of games, name of starting side of player (w/b), opponent to connect to, and optional command to suppress printing
    if len(sys.argv) < 4:
        print("Missing an arg")
        assert False
    num_games = sys.argv[1]
    side = sys.argv[2]
    opnt_data = sys_data[sys.argv[3]]
    self_data = sys_data[socket.gethostname()]
    engine = launchEngine(self_data['program'], self_data['threads'])
    #ip_addr = opnt_data['ip']
    #port = opnt_data['port']

    print_game = True
    if len(sys.argv) >= 5 and sys.argv[4] == 'noprint':
        print_game = False
    outcomes = []

    listen_socket = None
    game_socket = None
    if side == 'w':
        w_time = w_time * self_data['wattage']
        b_time = w_time * opnt_data['wattage']
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind((self_data['ip'], self_data['port']))#Currently just localhost connection
        listen_socket.listen()
        game_socket, addr = listen_socket.accept()
        print("Connection established by ", addr)
    elif side == 'b':
        b_time = w_time * self_data['wattage']
        w_time = w_time * opnt_data['wattage']
        game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        game_socket.connect((opnt_data['ip'], opnt_data['port']))
        print("Connection established to host")
    else:
        print("No valid argument for player side")
        assert False
    for i in range(num_games):
        if i%2 == 1:
            if side == 'w':
                side = 'b'
            else:
                side = 'w'
        #Reset state
        board = Board()
        b_time = 60000
        w_time = 60000
        game_over = False
        #make first move
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        my_move, time_used = getMove(engine, fen, b_time, w_time)
        fen, algebraic = board.playMove(my_move)
        if print_game:
            print(algebraic)
        w_time -= time_used
        if w_time <= 0:
            print("You fool! You used up all your time on your first move!")
            assert False
        data = bytes(my_move + ' ' + str(time_used), 'utf-8')
        game_socket.sendall(data)
        while not(game_over):
            data = game_socket.recv(1024)
            opponent_move = data.decode('utf-8').split()[0]
            opponent_time = float(data.decode('utf-8').split()[1])
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
                fen, algebraic = board.playMove(opponent_move)
                if print_game:
                    print(algebraic)
                my_move, time_used = getMove(engine, fen, b_time, w_time)
                if side == 'w':
                    if print_game:
                        print(clockTime(w_time), clockTime(b_time))
                    w_time -= time_used
                    if w_time <= 0:
                        my_move = "loss_time"
                else:
                    b_time -= time_used
                    if b_time <= 0:
                        my_move = "loss_time"
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
                    fen, algebraic = board.playMove(my_move)
                    if print_game:
                        print(algebraic)
                if print_game and side == 'b':
                    print(clockTime(w_time), clockTime(b_time))
                data = bytes(my_move + ' ' + str(time_used), 'utf-8')
                game_socket.sendall(data)
    game_socket.close()
    if not listen_socket is None:
        listen_socket.close()
    print(outcomes)
    score = 0
    for result in outcomes:
        if result == 'draw':
            score += 0.5
        elif result == 'loss_time' or result == 'loss_mate':
            score += 0
        elif result == 'win_mate' or result == 'win_time':
            score += 1
        else:
            print("Unrecognized results type:")
            print(result)
    score_str = str(score) + ' - ' + str(num_games - score)
    print("Final score is " + score_str)














