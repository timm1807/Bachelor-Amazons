from alpha_beta import iterative_deepening
from amazons_engine import AmazonsGame
from pvs import iterative_deepening_pvs
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

    # ------------- PVS -------------

    # Player 1: pvs.py | Player 2: Random moves
    def play_a_game_pvs_random(game):
        count = 0
        while True:
            if game.current_player == 1:
                best_move = iterative_deepening_pvs(game, 5, alpha_beta_player=game.current_player)
                if not best_move:
                    break
                print("Move Spieler 1 (PVS): ",best_move)
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

    # ------------- ALPHA BETA -------------

    # Player 1: Alpha Beta | Player 2: Random Moves
    #play_a_game_alphaBeta_random(game, max_depth=2)

    # Player 1: Alpha Beta DEBUG | Player 2: Random Moves
    #play_a_game_alphaBetaDEBUG_random(game, max_depth=1)

    # ------------- PVS -------------
 
    # Player 1: pvs.py | Player 2: Random moves # 45 Züge bis Win für PVS
    #play_a_game_pvs_random(game)


    # ------------ MCTS VS PVS ------------
    def play_game_ab_pvs(game, time_limit = 60):
        time_limit = time_limit
        # abwechselnd ab und pvs random welcher spieler 1 und 2
        alg_1_player = random.randint(1,2)
        move_count = 0
        move_stats_alg1 = {}
        move_stats_alg2 = {}
        iteration_count_alg1_list = {}
        iteration_count_alg2_list = {}
        winner = 0
        algo_1 = ""
        algo_2 = ""
        while True:
            #if alg_1_player == 1:
            algo_1 = "Alpha Beta Algorithmus"
            algo_2 = "PVS"
            if game.current_player == 1:
                    best_move, iteration_count_alg1 = iterative_deepening(game, 5, alpha_beta_player=game.current_player, time_limit=time_limit)
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
                    #iteration_count_alg1_list.append(iteration_count_alg1)
                    iteration_count_alg1_list[str(move_count)] = iteration_count_alg1
            else:
                best_move, iteration_count_alg2 = iterative_deepening_pvs(game, max_depth=5, alpha_beta_player=game.current_player, time_limit=time_limit)
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
                #iteration_count_alg2_list.append(iteration_count_alg2)
                iteration_count_alg2_list[str(move_count)] = iteration_count_alg2

        #winner = 2 if game.current_player == 1 else 1
        return move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit
    
    def play_game_pvs_ab(game, time_limit = 60):
        time_limit = time_limit
        # abwechselnd ab und pvs random welcher spieler 1 und 2
        alg_1_player = random.randint(1,2)
        move_count = 0
        move_stats_alg1 = {}
        move_stats_alg2 = {}
        iteration_count_alg1_list = {}
        iteration_count_alg2_list = {}
        winner = 0
        algo_1 = ""
        algo_2 = ""
        while True:
            #if alg_1_player == 1:
            algo_1 = "PVS"
            algo_2 = "Alpha Beta Algorithmus"
            if game.current_player == 1:
                    best_move, iteration_count_alg1 = iterative_deepening_pvs(game, max_depth=5, alpha_beta_player=game.current_player, time_limit=time_limit)
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
                best_move, iteration_count_alg2 = iterative_deepening(game, 5, alpha_beta_player=game.current_player, time_limit=time_limit)
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

        return move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit
    
    # Funktion zum Speichern der Spiele in einer JSON-Datei
    def save_game_stats(game_count, move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit, filename='game_stats.json'):
        filename_final = os.path.join(r"C:\Users\Timmy\Desktop\AB PVS", filename)
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


    ################## AB VS PVS 60 SEC ##################
    def ab_pvs_60():
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

        """
        while True:
            print(f"Spiel {game_count} beginnt")
            game = AmazonsGame()
            
            # MCTS VS PVS
            move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit = play_game_ab_pvs(game)

            # Speichere die Statistiken in einer JSON-Datei
            save_game_stats(game_count, move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit, filename="game_stats_ab_pvs_60.json")

            game_count += 1

            # Testweise nur eine bestimmte Anzahl Spiele spielen
            if game_count > 25:  # Beispiel: Stoppe nach 5 Spielen
                break

            time.sleep(time_limit)
        """
        game_count = 44
        while True:
            print(f"Spiel {game_count} beginnt")
            game = AmazonsGame()

            # PVS VS MCTS
            move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit = play_game_pvs_ab(game)

            # Speichere die Statistiken in einer JSON-Datei
            save_game_stats(game_count, move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit, filename="game_stats_ab_pvs_60.json")

            game_count += 1

            if game_count > 50:  # Beispiel: Stoppe nach 10 Spielen
                break

            time.sleep(time_limit)

    ################## AB VS PVS 30 SEC ##################
    def ab_pvs_30():
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
            
            # MCTS VS PVS
            move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit = play_game_ab_pvs(game, time_limit=30)

            # Speichere die Statistiken in einer JSON-Datei
            save_game_stats(game_count, move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit, filename="game_stats_ab_pvs_30.json")

            game_count += 1

            # Testweise nur eine bestimmte Anzahl Spiele spielen
            if game_count > 25:  # Beispiel: Stoppe nach 5 Spielen
                break

            time.sleep(time_limit)
        #"""
        #game_count = 4
        while True:
            print(f"Spiel {game_count} beginnt")
            game = AmazonsGame()

            # PVS VS MCTS
            move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit = play_game_pvs_ab(game, time_limit=30)

            # Speichere die Statistiken in einer JSON-Datei
            save_game_stats(game_count, move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit, filename="game_stats_ab_pvs_30.json")

            game_count += 1

            if game_count > 50:  # Beispiel: Stoppe nach 10 Spielen
                break

            time.sleep(time_limit)

    # 44
    ab_pvs_60()
    ab_pvs_30()