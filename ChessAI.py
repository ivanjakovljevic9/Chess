import random as r

def find_random_move(valid_moves):
    return valid_moves[(r.randint(0, len(valid_moves)-1))]