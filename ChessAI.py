import random as r

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
checkmate = 1000
stalemate = 0
max_depth = 2

def find_random_move(valid_moves):
    return valid_moves[(r.randint(0, len(valid_moves)-1))]


def find_best_move_random(gs, valid_moves):
    turn_multiplier = 1 if gs.white_to_move else -1
    opponent_min_max_score = checkmate
    best_player_move = None
    r.shuffle(valid_moves)
    for player_move in valid_moves:
        gs.make_move(player_move)
        opponents_moves = gs.get_valid_moves()
        if gs.stalemate:
            opponent_max_score = stalemate
        elif gs.checkmate:
            opponent_max_score = -checkmate
        else:
            opponent_max_score = -checkmate
            for opponent_move in opponents_moves:
                gs.make_move(opponent_move)
                gs.get_valid_moves()
                if gs.checkmate:
                    score = checkmate
                elif gs.stalemate:
                    score = stalemate
                else:
                    score = score_board(gs) * -turn_multiplier
                if score > opponent_max_score:
                    opponent_max_score = score
                gs.undo_move()
        if opponent_min_max_score > opponent_max_score:
            opponent_min_max_score = opponent_max_score
            best_player_move = player_move
        gs.undo_move()
    return best_player_move

def find_best_move(gs, valid_moves):
    global next_move
    next_move = None
    r.shuffle(valid_moves)
    find_move_nega_max_alpha_beta(gs, valid_moves, max_depth, -checkmate, checkmate, 1 if gs.white_to_move else -1)
    return next_move

def find_move_nega_max(gs, valid_moves, depth, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(gs)
    max_score = -checkmate
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_nega_max(gs, next_moves, depth - 1, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == max_depth:
                next_move = move
        gs.undo_move()
    return max_score

def find_move_nega_max_alpha_beta(gs, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(gs)
    max_score = -checkmate
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_nega_max_alpha_beta(gs, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == max_depth:
                next_move = move
        gs.undo_move()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def score_board(gs):
    if gs.checkmate:
        if gs.white_to_move:
            return -checkmate
        else:
            return checkmate
    elif gs.stalemate:
        return stalemate
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == "w":
                score += piece_score[square[1]]
            elif square[0] == "b":
                score -= piece_score[square[1]]
    return score