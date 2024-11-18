from threading import Timer
import hashlib
import time
import random

timeout = False
call_count = 0  # Variable zum Zählen der Aufrufe
hit_count = 0
actual_hit = 0
transposition_table = {}

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

# Anzahl der Reihen und Spalten des Bretts (angenommen für ein Schachbrett 8x8)
ROWS = 10
COLS = 10

# Initialisiere das Zobrist-Array
zobrist_table = [[random.getrandbits(64) for _ in range(4)] for _ in range(ROWS * COLS)]

def zobrist_hash(board):
    """
    Berechnet den Zobrist-Hash für das aktuelle Brett.

    Parameters
    ----------
    board : list
        Die aktuelle Brettkonfiguration

    Returns
    ----------
    int : Ein eindeutiger Zobrist-Hash-Wert für die Brettkonfiguration
    """
    h = 0
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece == 0:
                piece_type = 0  # Leeres Feld
            elif piece == 1:
                piece_type = 1  # Spieler 1
            elif piece == 2:
                piece_type = 2  # Spieler 2
            elif piece == "X":
                piece_type = 3  # Pfeil
            else:
                continue  # Für den Fall, dass ein ungültiges Feldzeichen vorhanden ist
            index = row * COLS + col
            h ^= zobrist_table[index][piece_type]
    return h

def incremental_zobrist_update(current_hash, move, board):
    """
    Aktualisiert den Zobrist-Hash-Wert inkrementell basierend auf dem gegebenen Zug.
    
    Parameters
    ----------
    current_hash : int
        Der aktuelle Zobrist-Hash-Wert des Brettes vor dem Zug.
    move : tuple
        Der Zug, dargestellt als ((sx, sy), (ex, ey), (ax, ay)), wobei s für Startposition, e für Endposition und a für Arrowposition steht.
    board : list
        Die aktuelle Brettkonfiguration.

    Returns
    ----------
    int : Der aktualisierte Zobrist-Hash-Wert nach dem Zug.
    """
    (sx, sy), (ex, ey), (ax, ay) = move

    # Identifiziere die Spieler- und Pfeiltypen auf dem Brett
    piece_start = board[sx][sy]  # Spieler, der den Zug startet
    piece_end = 0  # Nach dem Zug wird die Startposition leer sein
    arrow_piece = "X"  # Pfeil wird an die neue Position gesetzt

    # Aktualisiere den Hash durch XOR an der Startposition
    index_start = sx * COLS + sy
    current_hash ^= zobrist_table[index_start][piece_start]  # Entferne das Stück an der Startposition

    # Aktualisiere den Hash durch XOR an der Endposition
    index_end = ex * COLS + ey
    current_hash ^= zobrist_table[index_end][piece_start]  # Setze das Stück an die Endposition

    # Aktualisiere den Hash durch XOR an der Pfeilposition
    index_arrow = ax * COLS + ay
    current_hash ^= zobrist_table[index_arrow][3]  # Setze den Pfeil an die Pfeilposition

    # Führe den Zug auf dem Brett aus
    board[sx][sy] = 0  # Leere Startposition
    board[ex][ey] = piece_start  # Spieler an der Endposition
    board[ax][ay] = "X"  # Pfeil an der Pfeilposition

    return current_hash

def AAAAalpha_beta_pruning(game, depth, alpha, beta, maximizing_player, iteration_count, current_hash=None):
    global timeout, call_count, hit_count, actual_hit
    
    # Erhöhe den Aufrufzähler
    call_count += 1
    
    if timeout or depth == 0 or not game.current_player_has_legal_moves():
        return game.evaluate_position(), None
    
    # Initialisiere den Hash-Wert des aktuellen Brettes, falls nicht bereits vorhanden
    if current_hash is None:
        current_hash = zobrist_hash(game.board)
    
    if current_hash in transposition_table:
        hit_count += 1
        stored_depth, stored_eval, stored_move = transposition_table[current_hash]
        if stored_depth >= depth:
            actual_hit += 1
            return stored_eval, stored_move

    best_move = None
    if maximizing_player:
        game.current_player = 1
        moves = game.current_player_has_legal_moves()
        max_eval = float('-inf')
        for move in moves:
            # Kopiere das aktuelle Spiel und berechne den neuen Hash-Wert inkrementell
            simulated_game = game.copy()
            new_hash = incremental_zobrist_update(current_hash, move, simulated_game.board)
            simulated_game.make_move(*move)

            eval, _ = alpha_beta_pruning(simulated_game, depth-1, alpha, beta, False, iteration_count, new_hash)

            if eval > max_eval:
                max_eval = eval
                best_move = move
                if timeout:
                    transposition_table[current_hash] = (depth, max_eval, best_move)
                    return max_eval, best_move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        transposition_table[current_hash] = (depth, max_eval, best_move)
        return max_eval, best_move
    else:
        game.current_player = 2
        moves = game.current_player_has_legal_moves()
        min_eval = float('inf')
        for move in moves:
            # Kopiere das aktuelle Spiel und berechne den neuen Hash-Wert inkrementell
            simulated_game = game.copy()
            new_hash = incremental_zobrist_update(current_hash, move, simulated_game.board)
            simulated_game.make_move(*move)

            eval, _ = alpha_beta_pruning(simulated_game, depth-1, alpha, beta, True, iteration_count, new_hash)

            if eval < min_eval:
                min_eval = eval
                best_move = move
                if timeout:
                    transposition_table[current_hash] = (depth, min_eval, best_move)
                    return min_eval, best_move

            beta = min(beta, eval)
            if beta <= alpha:
                break

        transposition_table[current_hash] = (depth, min_eval, best_move)
        return min_eval, best_move

def alpha_beta_pruning(game, depth, alpha, beta, maximizing_player, iteration_count):
    global timeout, call_count, hit_count, actual_hit
    
    # Erhöhe den Aufrufzähler
    call_count += 1
    
    if timeout or depth == 0 or not game.current_player_has_legal_moves():
        return game.evaluate_position(), None
    
    #board_hash = zobrist_hash(game.board)
    board_hash = hash_board(game.board)
    if board_hash in transposition_table:
        hit_count += 1
        stored_depth, stored_eval, stored_move = transposition_table[board_hash]
        if stored_depth >= depth:
            actual_hit += 1
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


###################################

def iterative_deepening_transpos(game, max_depth, alpha_beta_player, time_limit):

    maximizing_player = True if alpha_beta_player == 1 else False

    global timeout, transposition_table, call_count, actual_hit, hit_count
    best_move = None
    transposition_table = {}
    set_timeout(time_limit)
    
    call_count = 0  # Zähler auf 0 setzen
    hit_count = 0
    actual_hit = 0

    for depth in range(1, max_depth + 1):
        if timeout:
            break
        eval, move = alpha_beta_pruning(game, depth, float('-inf'), float('inf'), maximizing_player, call_count)
        if not timeout:
            best_move = move
    
    print(len(transposition_table))
    #print(transposition_table)
    print(f"hit count: {hit_count}")
    print(f"actual hit count: {actual_hit}")
    return best_move, transposition_table