from threading import Timer
import hashlib
import time

timeout = False
call_count = 0  # Variable zum Zählen der Aufrufe

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

def pvs(game, depth, alpha, beta, maximizing_player, iteration_count, best_move_prev=None):
    global call_count
    global timeout

    # Erhöhe den Aufrufzähler
    call_count += 1
        
    if timeout or depth == 0 or not game.current_player_has_legal_moves():
        return game.evaluate_position(), None
    
    board_hash = hash_board(game.board)
    if board_hash in transposition_table:
        stored_depth, stored_eval, stored_move = transposition_table[board_hash]
        if stored_depth >= depth:
            return stored_eval, stored_move

    best_move = None
    first_move = True

    if maximizing_player:
        game.current_player = 1
        max_eval = float('-inf')

        # Hole alle Züge des aktuellen Spielers und füge den aus der vorherigen Iteration besten Zug als erstes hinzu
        moves = []
        if best_move_prev:
            moves.append(best_move_prev)
        for amazon in game.amazons[game.current_player]:
            for move in game.calculate_moves_for_amazon(amazon[0], amazon[1]):
                if move != best_move_prev:
                    moves.append(move)

        for move in moves:

            game.make_move(*move)
            if first_move:
                eval, _ = pvs(game, depth-1, alpha, beta, iteration_count, False) # Full window search
                first_move = False
            else:
                eval, _ = pvs(game, depth-1, alpha, alpha+1, iteration_count, False) # Null window search
                if eval > alpha:
                    eval, _ = pvs(game, depth-1, alpha, beta, iteration_count, False) # Full window search if necessary

            game.undo_move(*move)

            if eval > max_eval:
                max_eval = eval
                best_move = move
                if timeout:
                    transposition_table[board_hash] = (depth, max_eval, best_move)
                    return max_eval, best_move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        transposition_table[board_hash] = (depth, max_eval, best_move)
        return max_eval, best_move
    else:
        game.current_player = 2
        min_eval = float('inf')

        # Hole alle Züge des aktuellen Spielers und füge den aus der vorherigen Iteration besten Zug als erstes hinzu
        moves = []
        if best_move_prev:
            moves.append(best_move_prev)
        for amazon in game.amazons[game.current_player]:
            for move in game.calculate_moves_for_amazon(amazon[0], amazon[1]):
                if move != best_move_prev:
                    moves.append(move)

        for move in moves:

            game.make_move(*move)
            if first_move:
                eval, _ = pvs(game, depth-1, alpha, beta, iteration_count, True) # Full window search
                first_move = False
            else:
                eval, _ = pvs(game, depth-1, beta-1, beta, iteration_count, True) # Null window search
                if eval < beta:
                    eval, _ = pvs(game, depth-1, alpha, beta, iteration_count, True) # Full window search if necessary

            game.undo_move(*move)

            if eval < min_eval:
                min_eval = eval
                best_move = move
                if timeout:
                    transposition_table[board_hash] = (depth, min_eval, best_move)
                    return min_eval, best_move

            beta = min(beta, eval)
            if beta <= alpha:
                break
        transposition_table[board_hash] = (depth, min_eval, best_move)
        return min_eval, best_move

def iterative_deepening_pvs(game, max_depth, alpha_beta_player, time_limit):

    maximizing_player = True if alpha_beta_player == 1 else False

    global timeout, transposition_table, call_count
    best_move = None
    transposition_table = {}
    max_time = time_limit
    set_timeout(max_time)
    # Variable für den besten Zug der vorherigen Iteration
    best_move_prev = None

    call_count = 0

    for depth in range(1, max_depth + 1):
        if timeout:
            break
        eval, move = pvs(game, depth, float('-inf'), float('inf'), maximizing_player, call_count, best_move_prev)
        if not timeout:
            best_move = move
            best_move_prev = move
        
    return best_move, call_count


####################################################

def iterative_deepening_pvs_transpos(game, max_depth, alpha_beta_player, time_limit):

    maximizing_player = True if alpha_beta_player == 1 else False

    global timeout, transposition_table, call_count
    best_move = None
    transposition_table = {}
    max_time = time_limit
    set_timeout(max_time)
    # Variable für den besten Zug der vorherigen Iteration
    best_move_prev = None

    call_count = 0

    for depth in range(1, max_depth + 1):
        if timeout:
            break
        eval, move = pvs(game, depth, float('-inf'), float('inf'), maximizing_player, call_count, best_move_prev)
        if not timeout:
            best_move = move
            best_move_prev = move
    
    return best_move, transposition_table