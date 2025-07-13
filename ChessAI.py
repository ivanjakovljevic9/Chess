import random
import random as r

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
checkmate = 1000
stalemate = 0


def find_random_move(valid_moves):
    return valid_moves[(r.randint(0, len(valid_moves)-1))]


def find_best_move(gs, valid_moves):
    turn_multiplier = 1 if gs.white_to_move else -1
    opponent_min_max_score = checkmate
    best_player_move = None
    random.shuffle(valid_moves)
    for player_move in valid_moves:
        gs.make_move(player_move)
        opponents_moves = gs.get_valid_moves()
        opponent_max_score = -checkmate
        for opponent_move in opponents_moves:
            gs.make_move(opponent_move)
            if gs.checkmate:
                score = -turn_multiplier * checkmate
            elif gs.stalemate:
                score = stalemate
            else:
                score = score_material(gs.board) * -turn_multiplier
            if score > opponent_max_score:
                opponent_max_score = score
            gs.undo_move()
        if opponent_min_max_score > opponent_max_score:
            opponent_min_max_score = opponent_max_score
            best_player_move = player_move
        gs.undo_move()
    return best_player_move


def score_material(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += piece_score[square[1]]
            elif square[0] == "b":
                score -= piece_score[square[1]]
    return score