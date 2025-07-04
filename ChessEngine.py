class game_state():
    def __init__(self):
        self.board = [
                ["bR","bN","bB","bQ","bK","bB","bN","bR"],
                ["bP","bP","bP","bP","bP","bP","bP","bP"],
                ["--","--","--","--","--","--","--","--"],
                ["--","--","--","--","--","--","--","--"],
                ["--","--","--","--","--","--","--","--"],
                ["--","--","--","--","--","--","--","--"],
                ["wP","wP","wP","wP","wP","wP","wP","wP"],
                ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.white_to_move = True
        self.move_log = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move


    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    def get_valid_moves(self):
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.white_to_move) and (turn == "b" and not self.white_to_move):
                    piece = self.board[r][c][1]
                    if piece == "P":
                        self.get_pawn_move(r,c,moves)
                    elif piece == "N":
                        self.get_knight_move(r,c,moves)
                    elif piece == "B":
                        self.get_bishop_move(r,c,moves)
                    elif piece == "R":
                        self.get_rook_move(r,c,moves)
                    elif piece == "Q":
                        self.get_queen_move(r, c, moves)
                    elif piece == "K":
                        self.get_king_move(r, c, moves)
        return moves

    def get_pawn_move(self, r, c, moves):
        pass
    def get_knight_move(self, r, c, moves):
        pass
    def get_bishop_move(self, r, c, moves):
        pass
    def get_rook_move(self, r, c, moves):
        pass
    def get_queen_move(self, r, c, moves):
        pass
    def get_king_move(self, r, c, moves):
        pass



class move():

    ranks_to_rows = {"1": 7, "2":6, "3":5, "4":4, "5":3,
                     "6":2, "7":1, "8":0}
    rows_to_ranks = {v:k for k,v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4,
                     "f": 5, "g": 6, "h": 7}
    cols_to_files = {v:k for k,v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file((self.end_row, self.end_col))

    def get_rank_file(self,r,c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]