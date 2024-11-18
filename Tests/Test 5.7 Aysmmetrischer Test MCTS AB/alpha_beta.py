from threading import Timer
import hashlib
import time
import random

timeout = False
call_count = 0  # Variable zum Zählen der Aufrufe
temp = 0

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

def alpha_beta_pruning(game, depth, alpha, beta, maximizing_player, iteration_count):
    global timeout, call_count, temp
    
    # Erhöhe den Aufrufzähler
    call_count += 1
    
    if timeout or depth == 0 or not game.current_player_has_legal_moves():
        return game.evaluate_position(), None
    
    #board_hash = zobrist_hash(game.board)
    board_hash = hash_board(game.board)
    if board_hash in transposition_table:
        stored_depth, stored_eval, stored_move = transposition_table[board_hash]
        if stored_depth >= depth:
            return stored_eval, stored_move

    best_Move = None
    if maximizing_player:
        game.current_player = 1
        moves = game.current_player_has_legal_moves()
        max_eval = float('-inf')
        for move in moves:

            simulated_game = game.copy()
            simulated_game.make_move(*move)
            eval, _ = alpha_beta_pruning(simulated_game, depth-1, alpha, beta, False, iteration_count)

            if eval > max_eval:
                max_eval = eval
                best_Move = move
                if timeout:
                    transposition_table[board_hash] = (depth, max_eval, best_Move)
                    return max_eval, best_Move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        transposition_table[board_hash] = (depth, max_eval, best_Move)
        return max_eval, best_Move
    else:
        game.current_player = 2
        moves = game.current_player_has_legal_moves()
        min_eval = float('inf')
        for move in moves:

            simulated_game = game.copy()
            simulated_game.make_move(*move)
            eval, _ = alpha_beta_pruning(simulated_game, depth-1, alpha, beta, True, iteration_count)

            if eval < min_eval:
                min_eval = eval
                best_Move = move
                if timeout:
                    transposition_table[board_hash] = (depth, min_eval, best_Move)
                    return min_eval, best_Move

            beta = min(beta, eval)
            if beta <= alpha:
                break

        transposition_table[board_hash] = (depth, min_eval, best_Move)
        return min_eval, best_Move
    
def iterative_deepening(game, max_depth, alpha_beta_player, time_limit):

    maximizing_player = True if alpha_beta_player == 1 else False

    global timeout, transposition_table, call_count
    best_move = None
    transposition_table = {}
    set_timeout(time_limit)
    
    call_count = 0  # Zähler auf 0 setzen

    for depth in range(1, max_depth + 1):
        if timeout:
            break
        eval, move = alpha_beta_pruning(game, depth, float('-inf'), float('inf'), maximizing_player, call_count)
        if not timeout:
            best_move = move
        
    return best_move, call_count
