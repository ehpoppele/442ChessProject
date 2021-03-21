from Board import *

if __name__ == '__main__':
    board = Board()
    #Play a game including moving, capturing, en passant, and castling
    print(board.playMove("e2e4"))
    print(board.playMove("e7e5"))
    print(board.playMove("g1f3"))
    print(board.playMove("b8c6"))
    print(board.playMove("f1c4"))
    print(board.playMove("f8c5"))
    print(board.playMove("e1g1"))
    print(board.playMove("f7f5"))
    print(board.playMove("e4f5"))
    print(board.playMove("g7g5"))
    print(board.playMove("f5g6"))
    """
    while True:
        move = input("input move: ")
        if move == "q":
            break
        else:
            print(board.playMove(move))
    """