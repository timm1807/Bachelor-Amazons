from alpha_beta import iterative_deepening
from amazons_engine import AmazonsGame
from mcts3 import mcts3
import random
import time

import json
import os

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

    # ------------- ALPHA BETA -------------

    #"""
    # Player 1: Alpha Beta | Player 2: Random Moves
    def play_a_game_alphaBeta_random(game,max_depth):
        count = 0
        while True:
            if game.current_player == 1:
                best_move, _ = iterative_deepening(game, max_depth, alpha_beta_player=game.current_player, time_limit=120)
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

    """
    while True:
        game = AmazonsGame()
        play_a_game(game)
        time.sleep(30.0)
    """

    # ------------- MCTS -------------

    # Player 1: mcts3.py | Player 2: Random Moves
    def play_a_game_mcts3_random(game):
        count = 0
        while True:
            if game.current_player == 1:
                best_move = mcts3(game, is_to_move=game.current_player)
                #best_move = root.best_action()
                if not best_move:
                    break
                print("Move Spieler 1 (MCTS 3): ", best_move)
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

    # ------------- PVS -------------

    # ------------- MTD(f) -------------

    # ------------- ALPHA BETA -------------

    # Player 1: Alpha Beta | Player 2: Random Moves
    #play_a_game_alphaBeta_random(game, max_depth=2)

    # Player 1: Alpha Beta DEBUG | Player 2: Random Moves
    #play_a_game_alphaBetaDEBUG_random(game, max_depth=1)

    # ------------- MCTS -------------
    
    # Player 1: mcts2.py | Player 2: Random Moves
    #play_a_game_mcts2_random(game)

    # --- MCTS 3.0
    # Player 1: mcts3.py | Player 2: Random Moves
    #play_a_game_mcts3_random(game)


    # Player 1: mcts2_normal.py | Player 2: Random Moves
    #######play_a_game_mctsNormal_random(game)

    # Player 1: Random Moves | Player 2: mcts_normal.py
    #play_a_game_random_mctsNormal(game)
    
    # Player 1: mcts2.py | Player 2: Alpha Beta - 6 : 2 (81,79,65,85,75,83,70,63)
    #play_a_game_mcts2_alphaBeta(game)

    # Player 1: Alpha Beta | Player 2: mcts2.py
    #play_a_game_alphabeta_mcts2(game)

    # Player 1: mcts2.py | Player 2: mcts2_normal.py
    #play_a_game_mcts2_mcts2Normal(game)

    # Player 1: mcts2_normal.py | Player 2: mcts2.py
    #play_a_game_mcts2Normal_mcts2(game)

    # Player 1: mcts_normal.py | Player 2: mcts2_normal.py
    #play_a_game_mcts_mcts_normals(game)

    # Player 1: mcts2.py | Player 2: mcts2.py
    #play_a_game_mcts2_mcts_2(game)

    # ------------- PVS -------------
 
    # Player 1: pvs.py | Player 2: Random moves # 45 Züge bis Win für PVS
    #play_a_game_pvs_random(game)

    # ------------- MTD(f) -------------

    # Player 1: mtdf.py | Player 2: Random moves
    #play_a_game_mtdf_random(game, max_depth=2)


    """
    # Player 1: mtdf2.py | Player 2: Random moves
    def play_a_game_mtdf2_random(game):
        count = 0
        while True:
            if game.current_player == 1:
                best_move = iterative_deepening_mtdf2(game, 5)
                if not best_move:
                    break
                print("Move Spieler 1 (Alpha Beta): ",best_move)
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
                print("Move Spieler 2 (Random): ", move)
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
    
    #play_a_game_mtdf2_random(game)
    """

    #######################################################  TESTING   #############################################################
    # Player 1: mcts3.py

    def playTest():
        count = 0
        move_stats = {}
        while True:
            game = AmazonsGame()
            print(f"------------ STATS {count} ------------")
            eval, best_move = play_a_game_mcts3_move(game, move_stats)
            print(f"Zug: {best_move}")
            print(f"Bewertung: {eval}")
            count = count + 1
            print(f"Aktuelle Zug-Statistiken: {move_stats}")

    def play_a_game_mcts3_move(game, move_stats):
        best_move = mcts3(game, is_to_move=game.current_player)

        game.make_move(*best_move)
        eval = game.evaluate_position()

        if best_move in move_stats:
            move_stats[best_move]['count'] += 1
            # Nur hinzufügen, wenn der Bewertungswert nicht schon in der Liste ist
            if eval not in move_stats[best_move]['evals']:
                move_stats[best_move]['evals'].append(eval)
        else:
            move_stats[best_move] = {'count': 1, 'evals': [eval]}  # eval direkt hinzufügen, wenn es ein neuer Zug ist
    
        return eval, best_move
    
    #playTest()


    # ------------ MCTS VS ALPHA BETA ------------
    def play_game_mcts_alphabeta(game, time_limit = 60):
        time_limit = time_limit
        # abwechselnd mcts3 und alpha beta random welcher spieler 1 und 2
        algorithm_1_is_player_number = random.randint(1,2)
        move_count = 0
        move_stats_alg1 = {}
        move_stats_alg2 = {}
        iteration_count_alg1_list = {}
        iteration_count_alg2_list = {}
        winner = 0
        algo_1 = ""
        algo_2 = ""
        while True:
            #if algorithm_1_is_player_number == 1:
            algo_1 = "Monte-Carlo Tree Search"
            algo_2 = "Alpha-Beta Algorithm"
            if game.current_player == 1:
                best_move, iteration_count_alg1 = mcts3(game, is_to_move=game.current_player, time_limit=time_limit)
                if not best_move:
                    winner = 2
                    break
                game.make_move(*best_move)
                game.current_player = 2
                game.prev_move = best_move
                ##### STATS #####
                move_count += 1
                eval = game.evaluate_position()
                if best_move in move_stats_alg1:
                    move_stats_alg1[best_move]['count'] += 1
                    if eval not in move_stats_alg1[best_move]['evals']:
                        move_stats_alg1[best_move]['evals'].append(eval)
                else:
                    move_stats_alg1[best_move] = {'count': 1, 'evals': [eval]}
                iteration_count_alg1_list[str(move_count)] = iteration_count_alg1
            else:
                best_move, iteration_count_alg2 = iterative_deepening(game, max_depth=5, alpha_beta_player=game.current_player, time_limit=time_limit)
                if not best_move:
                    winner = 1
                    break
                game.make_move(*best_move)
                game.current_player = 1
                game.prev_move = best_move
                ##### STATS #####
                move_count += 1
                eval = game.evaluate_position()
                if best_move in move_stats_alg2:
                    move_stats_alg2[best_move]['count'] += 1
                    if eval not in move_stats_alg2[best_move]['evals']:
                        move_stats_alg2[best_move]['evals'].append(eval)
                else:
                    move_stats_alg2[best_move] = {'count': 1, 'evals': [eval]}
                iteration_count_alg2_list[str(move_count)] = iteration_count_alg2
            #else:
            """
            algo_1 = "Alpha-Beta Algorithm"
            algo_2 = "Monte-Carlo Tree Search"
            if game.current_player == 1:
                best_move, iteration_count_alg2 = iterative_deepening(game, max_depth=5, alpha_beta_player=game.current_player, time_limit=time_limit)
                if not best_move:
                    winner = 2
                    break
                game.make_move(*best_move)
                game.current_player = 2
                game.prev_move = best_move
                ##### STATS #####
                move_count += 1
                eval = game.evaluate_position()
                if best_move in move_stats_alg2:
                    move_stats_alg2[best_move]['count'] += 1
                    if eval not in move_stats_alg2[best_move]['evals']:
                        move_stats_alg2[best_move]['evals'].append(eval)
                else:
                    move_stats_alg2[best_move] = {'count': 1, 'evals': [eval]}
                iteration_count_alg2_list[str(move_count)] = iteration_count_alg2
            else:
                best_move, iteration_count_alg1 = mcts3(game, is_to_move=game.current_player, time_limit=time_limit)
                if not best_move:
                    winner = 1
                    break
                game.make_move(*best_move)
                game.current_player = 1
                game.prev_move = best_move
                ##### STATS #####
                move_count += 1
                eval = game.evaluate_position()
                if best_move in move_stats_alg1:
                    move_stats_alg1[best_move]['count'] += 1
                    if eval not in move_stats_alg1[best_move]['evals']:
                        move_stats_alg1[best_move]['evals'].append(eval)
                else:
                    move_stats_alg1[best_move] = {'count': 1, 'evals': [eval]}
                iteration_count_alg1_list[str(move_count)] = iteration_count_alg1
            """

        #winner = 2 if game.current_player == 1 else 1
        return move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit
    
    def play_game_alphabeta_mcts(game, time_limit = 60):
        time_limit = time_limit
        # abwechselnd mcts3 und alpha beta random welcher spieler 1 und 2
        algorithm_1_is_player_number = random.randint(1,2)
        move_count = 0
        move_stats_alg1 = {}
        move_stats_alg2 = {}
        iteration_count_alg1_list = {}
        iteration_count_alg2_list = {}
        winner = 0
        algo_1 = ""
        algo_2 = ""
        while True:
            algo_1 = "Alpha-Beta Algorithm"
            algo_2 = "Monte-Carlo Tree Search"
            if game.current_player == 1:
                best_move, iteration_count_alg1 = iterative_deepening(game, max_depth=5, alpha_beta_player=game.current_player, time_limit=time_limit)
                if not best_move:
                    winner = 2
                    break
                game.make_move(*best_move)
                game.current_player = 2
                game.prev_move = best_move
                ##### STATS #####
                move_count += 1
                eval = game.evaluate_position()
                if best_move in move_stats_alg1:
                    move_stats_alg1[best_move]['count'] += 1
                    if eval not in move_stats_alg1[best_move]['evals']:
                        move_stats_alg1[best_move]['evals'].append(eval)
                else:
                    move_stats_alg1[best_move] = {'count': 1, 'evals': [eval]}
                iteration_count_alg1_list[str(move_count)] = iteration_count_alg1
            else:
                best_move, iteration_count_alg2 = mcts3(game, is_to_move=game.current_player, time_limit=time_limit)
                if not best_move:
                    winner = 1
                    break
                game.make_move(*best_move)
                game.current_player = 1
                game.prev_move = best_move
                ##### STATS #####
                move_count += 1
                eval = game.evaluate_position()
                if best_move in move_stats_alg2:
                    move_stats_alg2[best_move]['count'] += 1
                    if eval not in move_stats_alg2[best_move]['evals']:
                        move_stats_alg2[best_move]['evals'].append(eval)
                else:
                    move_stats_alg2[best_move] = {'count': 1, 'evals': [eval]}
                iteration_count_alg2_list[str(move_count)] = iteration_count_alg2

        #winner = 2 if game.current_player == 1 else 1
        return move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit
    
    # Funktion zum Speichern der Spiele in einer JSON-Datei
    def save_game_stats(game_count, move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit, filename='game_stats.json'):
        filename_final = os.path.join(r"C:\Users\Timmy\Desktop\MCTS AB Simulation Value to 10", filename)
        try:
            # Convert tuple keys in move_stats to strings
            move_stats_str_keys_1 = {str(key): value for key, value in move_stats_alg1.items()}
            move_stats_str_keys_2 = {str(key): value for key, value in move_stats_alg2.items()}
            
            game_data = {
                'game_count': game_count,
                'move_count': move_count,
                'winner': winner,
                'time_limit': time_limit,
                'player_1': algo_1,
                'player_2': algo_2,
                'iteration_count_algo_1': iteration_count_alg1_list,
                'iteration_count_algo_2': iteration_count_alg2_list,
                'move_stats_alg1': move_stats_str_keys_1,
                'move_stats_alg2': move_stats_str_keys_2
            }

            # Überprüfe, ob die Datei bereits existiert
            if os.path.exists(filename_final):
                with open(filename_final, 'r') as file:
                    data = json.load(file)
            else:
                data = {}

            # Füge das neue Spiel zur Datenbank hinzu
            data[f'game_{game_count}'] = game_data

            # Speichere die Daten wieder in die JSON-Datei
            with open(filename_final, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Erfolgreich gespeichert: {filename_final}")
    
        except Exception as e:
            print(f"Fehler beim Speichern der Datei: {e}")


    ################## MCTS VS AB 60 SEC ##################
    def mcts_ab_60():
        # Wie viele Spiele gespielt wurden
        game_count = 1
        # SIEGQUOTE: Welcher Algorithmus hat wie oft gegenüber dem anderen gewonnen
        win_count = {"Spieler 1:": [],
                     "Spieler 2:": []}
        # ZUGQUALITÄT: Wie oft gute oder schlechtere Züge gespielt wurden
        move_stats = {}
        # MOVE COUNT
        move_count_overall = []
        # KNOTENEXPANSION: Wie viele Knoten durchiteriert wurden
        node_iteration_count = {"Spieler 1:": [],
                                "Spieler 2:": []}
        # LAUFZEIT BEI GEGEBENER ITERATIONSZAHL: Falls fixe Iterationsanzahl: wie schnell Knoten brauchen um diese Iterationszahl durchzuiterieren
        # Z.b. Iteration 0,1,2,3,4,5
        time_iteration = 0

        #"""
        while True:
            print(f"Spiel {game_count} beginnt")
            game = AmazonsGame()
            
            # MCTS VS ALPHA BETA
            move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit = play_game_mcts_alphabeta(game)

            # Speichere die Statistiken in einer JSON-Datei
            save_game_stats(game_count, move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit, filename='game_mcts_ab_60.json')

            game_count += 1

            # Testweise nur eine bestimmte Anzahl Spiele spielen
            if game_count > 5:  # Beispiel: Stoppe nach 5 Spielen
                break

            time.sleep(time_limit)
        #"""
        #game_count = 2
        while True:
            print(f"Spiel {game_count} beginnt")
            game = AmazonsGame()

            # ALPHA BETA VS MCTS
            move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit = play_game_alphabeta_mcts(game)

            # Speichere die Statistiken in einer JSON-Datei
            save_game_stats(game_count, move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit, filename='game_mcts_ab_60.json')

            game_count += 1

            if game_count > 10:  # Beispiel: Stoppe nach 10 Spielen
                break

            time.sleep(time_limit)

    ################## MCTS VS AB 30 SEC ##################
    def mcts_ab_30():
        # Wie viele Spiele gespielt wurden
        game_count = 1
        # SIEGQUOTE: Welcher Algorithmus hat wie oft gegenüber dem anderen gewonnen
        win_count = {"Spieler 1:": [],
                     "Spieler 2:": []}
        # ZUGQUALITÄT: Wie oft gute oder schlechtere Züge gespielt wurden
        move_stats = {}
        # MOVE COUNT
        move_count_overall = []
        # KNOTENEXPANSION: Wie viele Knoten durchiteriert wurden
        node_iteration_count = {"Spieler 1:": [],
                                "Spieler 2:": []}
        # LAUFZEIT BEI GEGEBENER ITERATIONSZAHL: Falls fixe Iterationsanzahl: wie schnell Knoten brauchen um diese Iterationszahl durchzuiterieren
        # Z.b. Iteration 0,1,2,3,4,5
        time_iteration = 0

        #"""
        while True:
            print(f"Spiel {game_count} beginnt")
            game = AmazonsGame()
            
            # MCTS VS AB
            move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit = play_game_mcts_alphabeta(game, time_limit=30)

            # Speichere die Statistiken in einer JSON-Datei
            save_game_stats(game_count, move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit, filename='game_mcts_ab_30.json')

            game_count += 1

            # Testweise nur eine bestimmte Anzahl Spiele spielen
            if game_count > 5:  # Beispiel: Stoppe nach 5 Spielen
                break

            time.sleep(time_limit)
        #"""
        #game_count = 9
        while True:
            print(f"Spiel {game_count} beginnt")
            game = AmazonsGame()

            # PVS VS MCTS
            move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit = play_game_alphabeta_mcts(game, time_limit=30)

            # Speichere die Statistiken in einer JSON-Datei
            save_game_stats(game_count, move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit, filename='game_mcts_ab_30.json')

            game_count += 1

            if game_count > 10:  # Beispiel: Stoppe nach 10 Spielen
                break

            time.sleep(time_limit)

    mcts_ab_60()
    mcts_ab_30()