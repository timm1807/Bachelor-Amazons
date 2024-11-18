from threading import Timer
import hashlib
import time

timeout = False

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

def alpha_beta_pruning(game, depth, alpha, beta, maximizing_player):
    global timeout
        
    if timeout or depth == 0 or not game.current_player_has_legal_moves():
        #print("Evaluating position for player... ",game.current_player)
        return game.evaluate_position(), None
    
    board_hash = hash_board(game.board)
    if board_hash in transposition_table:
        #print("board hash in transpostion_table TRUE")
        stored_depth, stored_eval, stored_move = transposition_table[board_hash]
        if stored_depth >= depth:
            return stored_eval, stored_move

    # Move ordering
    # moves = game.get_sorted_moves(game.current_player)

    best_Move = None
    if maximizing_player:
        game.current_player = 1
        max_eval = float('-inf')
        for amazon in game.amazons[game.current_player]:
            for move in game.calculate_moves_for_amazon(amazon[0], amazon[1]):

                game.make_move(*move)
                eval, _ = alpha_beta_pruning(game, depth-1, alpha, beta, False)
                game.undo_move(*move)

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
        min_eval = float('inf')
        for amazon in game.amazons[game.current_player]:
            for move in game.calculate_moves_for_amazon(amazon[0], amazon[1]):

                game.make_move(*move)
                eval, _ = alpha_beta_pruning(game, depth-1, alpha, beta, True)
                game.undo_move(*move)

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
    
def iterative_deepening(game, max_depth, alpha_beta_player):

    maximizing_player = True if alpha_beta_player == 1 else False

    global timeout, transposition_table
    best_move = None
    transposition_table = {}
    start_time = time.time()
    max_time = 60 # 30 sec oder 60 sec
    set_timeout(max_time)

    for depth in range(1, max_depth + 1):
        if timeout:
            break
        eval, move = alpha_beta_pruning(game, depth, float('-inf'), float('inf'), maximizing_player)
        if not timeout:
            best_move = move
        
    return best_move