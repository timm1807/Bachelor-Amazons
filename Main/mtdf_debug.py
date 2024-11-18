from threading import Timer
import hashlib
import time
from alpha_beta import iterative_deepening
import random

timeout = False
debug = False
debugA = False

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
    if debugA: print(f"-------- START ALPHA BETA - TIEFE: {depth} --------") ###
    global timeout, transposition_table
        
    if timeout or depth == 0 or not game.current_player_has_legal_moves():
        return game.evaluate_position(), None
    
    if debugA: print("TRANSPOSITION TABLES LOOKUP") ###
    board_hash = hash_board(game.board)
    entry = transposition_table.get(board_hash)

    # Falls Eintrag in der Transpositionstabelle, prüfen ob er nützlich ist
    if entry is not None and entry.depth >= depth:
        if entry.flag == EXACT:
            print(f"EXACT: value: {entry.value}")
            return entry.value, entry
        elif entry.flag == LOWERBOUND and entry.value >= beta:
            print(f"LOWERBOUND: value: {entry.value}")
            return entry.value, None  # Beta-Cutoff
        elif entry.flag == UPPERBOUND and entry.value <= alpha:
            print(f"UPPERBOUND: value: {entry.value}")
            return entry.value, None  # Alpha-Cutoff

    """
    # Falls wir einen Eintrag in der Transpositionstabelle haben, prüfen wir, ob er nützlich ist
    if board_hash in transposition_table:
        stored_depth, stored_eval, stored_move, stored_flag = transposition_table[board_hash]
        if stored_depth >= depth:
            if stored_flag == EXACT:
                print("RETURN BOARD VALUE")
                return stored_eval, stored_move
            elif stored_flag == LOWERBOUND and stored_eval >= beta:
                print("RETURN BOARD VALUE")
                return stored_eval, None  # Beta-Cutoff
            elif stored_flag == UPPERBOUND and stored_eval <= alpha:
                print("RETURN BOARD VALUE")
                return stored_eval, None  # Alpha-Cutoff
    """

    best_move = None
    if maximizing_player:

        if debugA: print(f"MAXIMIZING PLAYER") ###
        game.current_player = 1
        moves = game.current_player_has_legal_moves()
        max_eval = float('-inf')

        for move in moves:
            if debugA: print(f"Move: {move} wird angeguckt") ###

            simulated_game = game.copy()
            simulated_game.make_move(*move)
            eval, _ = alpha_beta_with_null_window(simulated_game, depth-1, alpha, beta, False)

            if debugA: print(f"EVAL of this MOVE: {move} | EVAL {eval} | NEW BEST MOVE? => {eval > max_eval} ") ###

            if eval > max_eval:
                max_eval = eval
                if debugA: print(f"NEUER BEST MOVE - {move}") ###
                best_move = move
                if timeout:
                    #transposition_table[board_hash] = (depth, max_eval, best_move, EXACT)
                    transposition_table.store(board_hash, max_eval, EXACT, depth)
                    #transposition_table[board_hash] = TranspositionTableEntry(max_eval, EXACT, depth)
                    if debugA: print("TIMEOUT") ###
                    return max_eval, best_move

            alpha = max(alpha, eval)
            if beta <= alpha:
                if debugA: print("BREAK BECAUSE OF BETA CUT-OFF") ###
                break

        flag = LOWERBOUND if max_eval >= beta else (UPPERBOUND if max_eval <= alpha else EXACT)
        #transposition_table[board_hash] = (depth, max_eval, best_move, flag)
        transposition_table.store(board_hash, max_eval, flag, depth)
        #transposition_table[board_hash] = TranspositionTableEntry(max_eval, flag, depth)
        if debugA: print(f"BEST MOVE: {best_move}") ###
        return max_eval, best_move
    else:

        if debugA: print(f"MINIMIZING PLAYER") ###
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
                    #transposition_table[board_hash] = (depth, min_eval, best_move, EXACT)
                    transposition_table.store(board_hash, min_eval, EXACT, depth)
                    #transposition_table[board_hash] = TranspositionTableEntry(max_eval, EXACT, depth)
                    return min_eval, best_move

            beta = min(beta, eval)
            if beta <= alpha:
                break

        flag = LOWERBOUND if min_eval >= beta else (UPPERBOUND if min_eval <= alpha else EXACT)
        #transposition_table[board_hash] = (depth, min_eval, best_move, flag)
        transposition_table.store(board_hash, min_eval, flag, depth)
        #transposition_table[board_hash] = TranspositionTableEntry(min_eval, flag, depth)
        return min_eval, best_move

def mtdf(game, f, depth, maximizing_player):
    if debug: print(f"f input: {f}")
    global timeout, transposition_table

    g = f
    upper_bound = float('inf')
    lower_bound = float('-inf')

    if debug: print(f"----START MTD(f)----") ###
    while lower_bound < upper_bound:
        if debug: print("WHILE ITERATION MTD(f)")
        if timeout:
            break
        if g == lower_bound:
            beta = g + 1
        else:
            beta = g

        if debug: print(f"##### g: {g}, f: {f}, alpha: {beta-1}, beta: {beta} #####") ###
        g, best_move = alpha_beta_with_null_window(game, depth, beta-1, beta, maximizing_player)
        if debug: print(f"After Alpha Beta: best_move: {best_move} | g: {g} | f: {f} | beta: {beta} | upper_bound: {upper_bound} | lower_bound: {lower_bound}")
        if g < beta:
            upper_bound = g
        else:
            lower_bound = g
        if debug: print(f"NOW: upper_bound: {upper_bound} | lower_bound: {lower_bound}")

    if debug: print(f"Best Move for this Depth: {best_move}") ###
    return g, best_move

def iterative_deepening_mtdf(game, max_depth, alpha_beta_player, time_limit=60):

    maximizing_player = True if alpha_beta_player == 1 else False

    global timeout, transposition_table
    best_move = None
    transposition_table = TranspositionTable()
    set_timeout(time_limit)

    """
    # Bewertet alle möglichen Züge
    evaluated_moves = []
    for move in game.current_player_has_legal_moves():
        simulated_game = game.copy()
        simulated_game.make_move(*move)
        evaluation = simulated_game.evaluate_position()
        evaluated_moves.append((evaluation, move))

    # Finde den maximalen Evaluationswert
    best_evaluation = max(evaluated_moves, key=lambda x: x[0])[0]
    
    f = best_evaluation  # Initialer Startwert für MTD(f)
    """
    f = 0
    #if debug: print("-iterative deepening start") ###
    
    for depth in range(1, max_depth + 1):
        print(f"DEPTH: {depth}") ###
        if timeout:
            #if debug: print("-TIMEOUT") ###
            break
        g, best_move = mtdf(game, f, depth, maximizing_player)
        print(f"best_move: {best_move}")
        f = g
        #print(f"f: {f}")
        
    return best_move
