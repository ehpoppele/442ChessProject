#Chess Board class for making and updating moves; minimal rules checking. Primary function is updating and converting to FEN after a move

class Board():

    def __init__(self):
        #Set initial board to starting position
        #Board looks weird but this way python indices match with board squares best
        self.board = [ ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                       ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                       ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                       ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'] ]
        self.castling_rights = [True, True, True, True] #indices correspond to castling for KQkq
        self.active_player = "w"
        self.half_moves = 0
        self.full_moves = 1
        self.en_passant_capture = '-'
        
    #Returns a tuple of piece name and player, or None if the square is empty
    def pieceAt(self, square):
        col = ord(square[0])-97
        row = int(square[1])-1
        piece = self.board[row][col]
        if piece == ' ':
            return(' ', None)
        else:
            if piece.isupper():
                return(piece, 'w')
            else:
                return(piece, 'b')
                
    #Checks a move to see if en Passant capture is allowed on next move; assumes the move given is a pawn move
    def updateEnPassant(self, move):
        if abs(int(move[3])-int(move[1])) != 2: #Assume a pawn, confirm move is 2 squares
            self.en_passant_capture = '-'
            return False
        else: #Check adjacent squares
            row = int(move[3])-1
            col_1 = ord(move[2])-96
            col_2 = ord(move[2])-98
            if col_1 > -1 and col_1 < 8: 
                piece = self.board[row][col_1]
                if piece.lower() == 'p' and ((piece.isupper() and self.active_player == "w") or (piece.islower() and self.active_player == "b")): #confirm piece is a pawn of opposite color
                    self.en_passant_capture = move[0] + str((int(move[3])+int(move[1]))//2)
                    return True
            if col_2 > -1 and col_2 < 8: 
                piece = self.board[row][col_2]
                if piece.lower() == 'p' and ((piece.isupper() and self.active_player == "w") or (piece.islower() and self.active_player == "b")):
                    self.en_passant_capture = move[0] + str((int(move[3])+int(move[1]))//2)
                    return True
    
    #Takes move and updates castling_rights
    def updateCastlingRights(self, move):
        target = move[0:2]
        destination = move[2:]
        #If any move starts or ends in one of the corners, then the rook has left that corner or been captured
        corners = ["h1", "a1", "h8", "a8"]
        for i in range(4):
            if target == corners[i] or destination == corners[i]:
                self.castling_rights[i] = False
        #If king moves, all castling is lost
        if self.pieceAt(target)[0].lower() == 'k':
            if self.pieceAt(target)[1] == 'w':
                self.castling_rights[0] = False
                self.castling_rights[1] = False
            else:
                self.castling_rights[2] = False
                self.castling_rights[3] = False
                
    #Returns false if the move given is not a castlingMove, otherwise updates the board and returns true
    def castlingMove(self, move):
        piece, _ = self.pieceAt(move[0:2])
        if piece.lower() != 'k':
            return False
        destination = move[2:]
        castle_destinations = ['g1', 'c1', 'g8', 'c8']
        #If it moved to a castle square while castling was legal, it must have castled
        #doing this in a loop is too tricky without better helper functions
        if destination == 'g1' and self.castling_rights[0]:
            self.board[0][4] = ' '
            self.board[0][7] = ' '
            self.board[0][6] = 'K'
            self.board[0][5] = 'R'
            return True
        if destination == 'c1' and self.castling_rights[1]:
            self.board[0][4] = ' '
            self.board[0][0] = ' '
            self.board[0][2] = 'k'
            self.board[0][3] = 'r'
            return True
        if destination == 'g8' and self.castling_rights[2]:
            self.board[7][4] = ' '
            self.board[7][7] = ' '
            self.board[7][6] = 'k'
            self.board[7][5] = 'r'
            return True
        if destination == 'c1' and self.castling_rights[1]:
            self.board[7][4] = ' '
            self.board[7][0] = ' '
            self.board[7][2] = 'k'
            self.board[7][3] = 'r'
            return True
        return False
        
    #Returns FEN notation for the current state of the game as a string
    def FEN(self):
        full_board = ''
        #Because of the weird board nature, we want to go through rows backwards and columns forward
        row = 7
        for i in range(8):
            for square in self.board[row-i]:
                full_board += square
            full_board += '/'
        #now replace spaces with numbers
        ret_str = ''
        spaces = 0
        for i in range(len(full_board)):
            if full_board[i] == ' ':
                spaces += 1
            else:
                if spaces > 0:
                    ret_str += str(spaces)
                    spaces = 0
                ret_str += full_board[i]
        ret_str += ' '
        ret_str += self.active_player
        ret_str += ' '
        castle_string = ''
        if self.castling_rights[0]:
            castle_string += 'K'
        if self.castling_rights[1]:
            castle_string += 'Q'
        if self.castling_rights[2]:
            castle_string += 'k'
        if self.castling_rights[3]:
            castle_string += 'q'
        if castle_string == '':
            castle_string = '-'
        ret_str += castle_string
        ret_str += ' '
        ret_str += self.en_passant_capture
        ret_str += ' '
        ret_str += str(self.half_moves)
        ret_str += ' '
        ret_str += str(self.full_moves)
        return ret_str
        
    #Takes move as a string and returns a FEN of game along with algebraic notation of the move
    #First version will allow illegal moves, I guess? in that we assume stockfish never gives us an illegal move
    #Will add stuff to allow castling later
    def playMove(self, move):
        #Get piece moved and confirm no immediate issues
        promotion = False
        if len(move) != 4:
            if len(move) == 5: #Promotion moves are 5 long and valid
                promotion = True
            else:
                print(move)
                print(self.FEN())
                assert False #Move should always be of the form xNyM(p), where x,y are in columns a-h and N, M in rows 1-8, p is promotion piece
        piece, player = self.pieceAt(move[0:2])
        assert player == self.active_player
        assert piece != ' '
        end_move = move[2:]
        if promotion:
            end_move = move[2:4]
        target, target_player = self.pieceAt(end_move)
        assert (target_player is None or target_player != self.active_player)
        
        #algebraic doesn't work for castling, check, or checkmate rn
        algebraic = end_move
        if target != ' ':
            algebraic = 'x' + algebraic
        if piece.lower() != 'p':
            algebraic = piece.upper() + algebraic
        else:
            algebraic = move[0:2] + algebraic
        if self.active_player == 'b':
            algebraic = "... " + algebraic
        algebraic = str(self.full_moves) + ". " + algebraic
        if promotion:
            algebraic += move[-1].upper()
        
        #update halfmoves
        if (piece.lower() != 'p' and target == ' '):
            self.half_moves += 1
        else:
            self.half_moves = 0 
            
        #update player and fullmoves
        if self.active_player == 'w':
            self.active_player = 'b'
        else:
            self.active_player = 'w'
            self.full_moves += 1
        
        self.updateCastlingRights(move)
        #Confirm move was not castling i.e. only one piece moved
        if not self.castlingMove(move): #This function already does the moving if it was castling
            self.board[int(move[1])-1][ord(move[0])-97] = ' '
            if promotion: 
                if self.active_player == 'w': #Active player has already changed, so we're using opposite
                    self.board[int(move[3])-1][ord(move[2])-97] = move[-1]
                else:
                    self.board[int(move[3])-1][ord(move[2])-97] = move[-1].upper()
            else:
                self.board[int(move[3])-1][ord(move[2])-97] = piece
        if (move[2:] + ' ') == self.en_passant_capture:
            if int(move[3])-1 == 5:
                self.board[4][ord(move[2])-97] = ' '
            elif int(move[3])-1 == 2:
                self.board[3][ord(move[2])-97] = ' '
            else: #Should never reach this case
                assert False
        self.updateEnPassant(move)
        
        #Stockfish will give None for bestmove if the game is over, so we only need to check 50 move rule and 3fold repetition
        if self.half_moves == 100:
            return 'draw', algebraic
        #Still need to check 3fold repetition rule here
        #This is my current solution to endless games
        if self.full_moves > 500:
            return 'draw', algebraic
        else:
            return self.FEN(), algebraic
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
