from threading import Timer
import hashlib
import time
from alpha_beta import iterative_deepening
import random

timeout = False
call_count = 0  # Variable zum Zählen der Aufrufe

class TranspositionTableEntry:
    def __init__(self, value, flag, depth):
        self.value = value  # gespeicherte Wert
        self.flag = flag    # Kennzeichnung: exact, lowerbound, upperbound
        self.depth = depth  # Tiefe der Suche, die diesen Wert gefunden hat

class TranspositionTable:
    def __init__(self):
        self.table = {}

    def get(self, key):
        return self.table.get(key)

    def store(self, key, value, flag, depth):
        self.table[key] = TranspositionTableEntry(value, flag, depth)

# Konstanten
EXACT = 0         # Exakter Wert
LOWERBOUND = 1    # Lower Bound
UPPERBOUND = 2    # upper Bound

def timeout_handler():
    global timeout
    timeout = True

def set_timeout(seconds):
    global timeout
    timeout = False
    timer = Timer(seconds, timeout_handler)
    timer.start()

def hash_board(board):
    """
    Erzeugt einen Hash-Wert für das aktuelle Brett, um es in der Transpositionstabelle zu speichern.

    Parameters
    ----------
    board : list
        Die aktuelle Brettkonfiguration

    Returns
    ----------
    str : Ein eindeutiger Hash-Wert für die Brettkonfiguration
    """
    board_str = ''.join(map(str, [item for sublist in board for item in sublist]))
    return hashlib.sha256(board_str.encode()).hexdigest()

def alpha_beta_with_null_window(game, depth, alpha, beta, maximizing_player):
    global timeout, transposition_table, call_count

    # Erhöhe den Aufrufzähler
    call_count += 1
        
    if timeout or depth == 0 or not game.current_player_has_legal_moves():
        return game.evaluate_position(), None
    
    board_hash = hash_board(game.board)
    entry = transposition_table.get(board_hash)

    # Falls Eintrag in Transpositionstabelle, prüfen ob er nützlich ist
    if entry is not None and entry.depth >= depth:
        if entry.flag == EXACT:
            return entry.value, entry
        elif entry.flag == LOWERBOUND and entry.value >= beta:
            return entry.value, None  # Beta-Cutoff
        elif entry.flag == UPPERBOUND and entry.value <= alpha:
            return entry.value, None  # Alpha-Cutoff

    best_move = None
    if maximizing_player:

        game.current_player = 1
        moves = game.current_player_has_legal_moves()
        max_eval = float('-inf')

        for move in moves:

            simulated_game = game.copy()
            simulated_game.make_move(*move)
            eval, _ = alpha_beta_with_null_window(simulated_game, depth-1, alpha, beta, False)

            if eval > max_eval:
                max_eval = eval
                best_move = move
                if timeout:
                    transposition_table.store(board_hash, max_eval, EXACT, depth)
                    return max_eval, best_move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        flag = LOWERBOUND if max_eval >= beta else (UPPERBOUND if max_eval <= alpha else EXACT)
        transposition_table.store(board_hash, max_eval, flag, depth)
        return max_eval, best_move
    else:

        game.current_player = 2
        moves = game.current_player_has_legal_moves()
        min_eval = float('inf')

        for move in moves:

            simulated_game = game.copy()
            simulated_game.make_move(*move)
            eval, _ = alpha_beta_with_null_window(simulated_game, depth-1, alpha, beta, True)

            if eval < min_eval:
                min_eval = eval
                best_move = move
                if timeout:
                    transposition_table.store(board_hash, min_eval, EXACT, depth)
                    return min_eval, best_move

            beta = min(beta, eval)
            if beta <= alpha:
                break

        flag = LOWERBOUND if min_eval >= beta else (UPPERBOUND if min_eval <= alpha else EXACT)
        transposition_table.store(board_hash, min_eval, flag, depth)
        return min_eval, best_move

def mtdf(game, f, depth, maximizing_player):
    global timeout, transposition_table

    g = f
    upper_bound = float('inf')
    lower_bound = float('-inf')

    while lower_bound < upper_bound:
        if timeout:
            break
        if g == lower_bound:
            beta = g + 1
        else:
            beta = g

        g, best_move = alpha_beta_with_null_window(game, depth, beta-1, beta, maximizing_player)

        if g < beta:
            upper_bound = g
        else:
            lower_bound = g

    return g, best_move

def iterative_deepening_mtdf(game, max_depth, alpha_beta_player, time_limit=60):

    maximizing_player = True if alpha_beta_player == 1 else False

    global timeout, transposition_table, call_count
    best_move = None
    transposition_table = TranspositionTable()
    set_timeout(time_limit)

    call_count = 0  # Zähler auf 0 setzen

    f = 0
    
    for depth in range(1, max_depth + 1):
        if timeout:
            break
        f, best_move = mtdf(game, f, depth, maximizing_player)

    return best_move, call_count
