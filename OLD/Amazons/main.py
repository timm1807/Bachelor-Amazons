from alpha_beta import alpha_beta_pruning, set_timeout, iterative_deepening
from amazons_engine import AmazonsGame
from mcts2 import mcts2
from mcts import MCTSNode, mcts
import random
import time

if __name__ == "__main__":

    game = AmazonsGame()
    
    # INIT OWN BOARD
    """
    #board = [['X', 'X', 'X', 1, 'X', 'X', 'X', 'X', 'X', 'X'], ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], [0, 'X', 0, 'X', 0, 'X', 'X', 'X', 1, 1], ['X', 'X', 0, 0, 'X', 'X', 'X', 'X', 'X', 2], [0, 0, 0, 2, 'X', 'X', 1, 0, 'X', 'X'], [0, 'X', 'X', 0, 'X', 'X', 'X', 0, 'X', 0], [0, 'X', 0, 0, 'X', 2, 0, 2, 0, 'X'], [0, 0, 'X', 0, 0, 'X', 0, 0, 'X', 0], [0, 0, 0, 'X', 0, 0, 'X', 0, 'X', 0], [0, 0, 0, 0, 'X', 'X', 0, 0, 0, 0]]
    # Vorteil Spieler 2
    #board = [['X', 'X', 0, 1, 'X', 'X', 'X', 'X', 'X', 'X'], ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], [0, 'X', 0, 'X', 0, 'X', 'X', 'X', 1, 1], ['X', 'X', 0, 0, 'X', 'X', 'X', 'X', 'X', 2], [0, 0, 0, 2, 'X', 'X', 1, 0, 'X', 'X'], [0, 'X', 'X', 0, 'X', 'X', 'X', 0, 'X', 0], [0, 'X', 0, 0, 'X', 2, 0, 2, 0, 'X'], [0, 0, 'X', 0, 0, 'X', 0, 0, 'X', 0], [0, 0, 0, 'X', 0, 0, 'X', 0, 'X', 0], [0, 0, 0, 0, 'X', 'X', 0, 0, 0, 0]]
    # Vorteil Spieler 1
    board = [['X', 'X', 0, 2, 'X', 'X', 'X', 'X', 'X', 'X'], ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], [0, 'X', 0, 'X', 0, 'X', 'X', 'X', 2, 2], ['X', 'X', 0, 0, 'X', 'X', 'X', 'X', 'X', 1], [0, 0, 0, 1, 'X', 'X', 2, 0, 'X', 'X'], [0, 'X', 'X', 0, 'X', 'X', 'X', 0, 'X', 0], [0, 'X', 0, 0, 'X', 1, 0, 1, 0, 'X'], [0, 0, 'X', 0, 0, 'X', 0, 0, 'X', 0], [0, 0, 0, 'X', 0, 0, 'X', 0, 'X', 0], [0, 0, 0, 0, 'X', 'X', 0, 0, 0, 0]]
    game.board = board
    game.amazons = game.find_positions()
    game.current_player = 1
    """

    game.print_board()
    
    # ------------- TESTING -------------
    #game.test_WrongMoves()
    #game.random_play()

    #game.get_sorted_moves(game.current_player)

    # Zug 1
    """
    move=((0,3),(5,8),(7,8)) # 1 2 True True (Müsste true)
    #move=((0,3),(2,1),(7,1)) # 0 2 False True (Müsste false)
    #move=((0,3),(6,3),(6,6)) # 3 3 False False (Müsste true)
    #move=((0,3),(5,8),(6,8)) # 1 2 True True (Müsste True)
    #move=((0,3),(4,3),(5,3)) # (Müsste false)
    # Angepasstes Board von oben
    #move=((4,6),(5,7),(6,6)) # Müsste (true)
    #move=((4,6),(5,7),(4,7)) # Müsste (False)
    """

    # Zug 2
    """
    game.make_move(*move)
    game.current_player = 2
    game.prev_move = move
    move=((6,9),(6,5),(4,7))
    """

    """ ---- Test für move_prev_blocked_amazon ----
    #move=((0,3),(5,8),(7,8)) # Zug 1 -> Erwarte eine 2
    #move=((0,3),(5,8),(9,8)) # Zug 1 -> Erwarte eine 1
    #move=((0,3),(0,2),(0,1)) # Zug 1 -> Erwarte eine 0
    #move=((4,6),(4,7),(5,7)) # Test mit init board - Erwarte eine 1
    #move=((4,6),(5,7),(6,6)) # Test mit init board - Erwarte eine 2
    move=((0,3),(0,2),(0,3)) # Test mit init board - Erwarte eine 0
    game.make_move(*move)
    game.prev_move = move
    game.current_player = 2
    #move=((6,9),(6,4),(9,4)) # Zug 2
    #move=((6,7),(6,6),(6,7)) # Test mit init board - Zug 2 (1)
    #move=((6,7),(7,6),(7,7)) # Test mit init board - Zug 2 (2)
    move=((6,7),(7,6),(7,7)) # Test mit init board - Zug 2 (0)
    """

    """ ------------- MOVE ORDERING TESTS -------------
    game.make_move(*move)
    game.print_board()
    print(f"Move blockt wie viele Amazonen: {game.move_blocks_opponent(move)}")
    print(f"Pfeil blockt wie viele Amazonen: {game.arrow_blocks_opponent(move)}")
    print(f"Amazone neben adj Amazone: {game.move_adjacent_to_opponent(move)}")
    print(f"Pfeil neben adj Amazone: {game.arrow_adj_to_opponent(move)}")
    print(f"Amazone mit Amazone und Pfeil blockiert: {game.blocking_amazon_multiple_ways(move)}")
    print(f"Amazone wurde wie oft durch prev Move blockiert: {game.move_prev_blocked_amazon(move)}")
    print(f"Gegnerische Amazone hat prev Move zu der jetzigen gemoved: {game.move_amazon_to_which_enemy_amazon_moved_adj(move)}")
    print(f"Gegnerischer Pfeil wurde prev Move zu der jetzigen geschossen:{game.move_amazon_to_which_enemy_arrow_moved_adj(move)}")
    print(f"Gegnr Amazone vom prev Move wird jetzt blockiert: {game.block_amazon_from_prev_move(move)}")
    print(f"Amazone wird nicht durch andere blockiert (Am Start): {game.move_not_blocking_any_opponent(move)}")
    """

    """ ----- ALPHA BETA TEST -----
    set_timeout(30.0)
    best_eval, best_move = alpha_beta_pruning(game, depth, alpha, beta, maximizing_player)
    game.make_move(*best_move) # *((0, 3), (0, 2), (0, 3)) -> (0,3) , (0,2) , (0,3)
    game.print_board()
    print(f"Beste Bewertung: {best_eval}")
    print(f"Bester Zug: {best_move}")
    """

    #################################################################################
    ################################ EVALUATION TEST ################################

    #game.make_move((0,3),(0,0),(0,1)) # -13.125 // SCHLECHTER ZUG -9.40041504
    #game.make_move((0,3),(6,3),(6,6)) # 46.95442708 // OKAY ZUG 56.45853271
    #game.make_move((0,3),(0,5),(1,6)) # -15.79361979 // NOCH SCHLECHTERER ZUG -10.69914374
    #game.print_board()
    #print(round(game.evaluate_position(), 8))

    #"""
    # Player 1: Alpha Beta | Player 2: Random Moves
    def play_a_game(game):
        count = 0
        while True:
            if game.current_player == 1:
                #set_timeout(30.0)
                #best_eval, best_move = alpha_beta_pruning(game, depth=3, alpha=float("-inf"), beta=float("inf"), maximizing_player=True)
                best_move = iterative_deepening(game, 5)
                if not best_move:
                    break
                print("Move Spieler 1: ",best_move)
                game.make_move(*best_move)
                print("EVAL ALPHA BETA 1: ",game.evaluate_position())
                game.current_player = 2
                count += 1
                game.print_board()
                game.prev_move = best_move
            else:
                all_legal_moves = game.current_player_has_legal_moves()
                if not all_legal_moves:
                    break
                move = random.choice(all_legal_moves)
                print("Move Spieler 2: ", move)
                game.make_move(*move)
                game.current_player = 1
                print("EVAL SPIELER 2: ",game.evaluate_position())
                count += 1
                game.print_board()
                game.prev_move = move
                print("---------------------------------------------------------------------")
        print(f"Spieler {game.current_player} hat keine legalen Züge mehr.")
        print("Game over")
        print(f"Gespielte Züge: {count}")
    
    #play_a_game(game)

    """
    while True:
        game = AmazonsGame()
        play_a_game(game)
        time.sleep(30.0)
    """

    # Player 1: mcts.py | Player 2: Random Moves
    def play_a_game_mcts(game, itermax=1000):
        count = 0
        while True:
            if game.current_player == 1:
                root = MCTSNode(game)
                best_move = mcts(root, itermax)
                if not best_move:
                    break
                print("Move Spieler 1 (MCTS): ", best_move)
                game.make_move(*best_move)
                game.current_player = 2
                count += 1
                game.print_board()
                game.prev_move = best_move
            else:
                all_legal_moves = game.current_player_has_legal_moves()
                if not all_legal_moves:
                    break
                move = random.choice(all_legal_moves)
                print("Move Spieler 2: ", move)
                game.make_move(*move)
                game.current_player = 1
                count += 1
                game.print_board()
                game.prev_move = move
                print("---------------------------------------------------------------------")
        print(f"Spieler {game.current_player} hat keine legalen Züge mehr.")
        print("Game over")
        print(f"Gespielte Züge: {count}")

    #play_a_game_mcts(game)

    # Player 1: mcts.py | Player 2: Alphabeta
    def play_a_game_mcts_alphabeta(game, itermax=10000):
        count = 0
        while True:
            if game.current_player == 1:
                root = MCTSNode(game)
                best_move = mcts(root, itermax)
                if not best_move:
                    break
                print("Move Spieler 1 (MCTS): ", best_move)
                game.make_move(*best_move)
                game.current_player = 2
                count += 1
                game.print_board()
                game.prev_move = best_move
            else:
                #set_timeout(30.0)
                #best_eval, best_move = alpha_beta_pruning(game, depth=3, alpha=float("-inf"), beta=float("inf"), maximizing_player=True)
                best_move = iterative_deepening(game, 5)
                if not best_move:
                    break
                print("Move Spieler 2 (Alpha Beta): ",best_move)
                game.make_move(*best_move)
                game.current_player = 1
                count += 1
                game.print_board()
                game.prev_move = best_move
                print("---------------------------------------------------------------------")
        print(f"Spieler {game.current_player} hat keine legalen Züge mehr.")
        print("Game over")
        print(f"Gespielte Züge: {count}")

    #play_a_game_mcts_alphabeta(game)

    # Player 1: mcts2.py | Player 2: Random Moves
    def play_a_game_mcts2(game):
        count = 0
        while True:
            if game.current_player == 1:
                best_move = mcts2(game, player=game.current_player)
                #best_move = root.best_action()
                if not best_move:
                    break
                print("Move Spieler 1 (MCTS): ", best_move)
                game.make_move(*best_move)
                game.current_player = 2
                print("EVAL SPIELER 1: ",game.evaluate_position())
                count += 1
                game.print_board()
                game.prev_move = best_move
            else:
                all_legal_moves = game.current_player_has_legal_moves()
                if not all_legal_moves:
                    break
                move = random.choice(all_legal_moves)
                print("Move Spieler 2: ", move)
                game.make_move(*move)
                game.current_player = 1
                print("EVAL SPIELER 2: ",game.evaluate_position())
                count += 1
                game.print_board()
                game.prev_move = move
                print("---------------------------------------------------------------------")
        print(f"Spieler {game.current_player} hat keine legalen Züge mehr.")
        print("Game over")
        print(f"Gespielte Züge: {count}")

    #play_a_game_mcts2(game)

    # Player 1: mcts2.py | Player 2: Alpha Beta
    def play_a_game_mcts_alpha(game):
        count = 0
        while True:
            if game.current_player == 1:
                best_move = mcts2(game, player=game.current_player)
                #best_move = root.best_action()
                if not best_move:
                    break
                print("Move Spieler 1 (MCTS): ", best_move)
                game.make_move(*best_move)
                game.current_player = 2
                print("EVAL SPIELER 1: ",game.evaluate_position())
                count += 1
                game.print_board()
                game.prev_move = best_move
            else:
                #set_timeout(30.0)
                #best_eval, best_move = alpha_beta_pruning(game, depth=3, alpha=float("-inf"), beta=float("inf"), maximizing_player=True)
                best_move = iterative_deepening(game, 5, alpha_beta_player=game.current_player)
                if not best_move:
                    break
                print("Move Spieler 2 (Alpha Beta): ",best_move)
                game.make_move(*best_move)
                game.current_player = 1
                count += 1
                game.print_board()
                game.prev_move = best_move
                print("---------------------------------------------------------------------")
        print(f"Spieler {game.current_player} hat keine legalen Züge mehr.")
        print("Game over")
        print(f"Gespielte Züge: {count}")

    play_a_game_mcts_alpha(game)