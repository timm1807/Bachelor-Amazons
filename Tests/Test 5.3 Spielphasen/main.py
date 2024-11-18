from amazons_engine import AmazonsGame
from mtdf import iterative_deepening_mtdf
from alpha_beta import iterative_deepening
from pvs import iterative_deepening_pvs
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


    # ------------ ab VS mtdf ------------
    def play_game_ab_mtdf(game, time_limit = 60):
        time_limit = time_limit
        # abwechselnd ab3 und mtdf random welcher spieler 1 und 2
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
            algo_1 = "Alpha Beta Algorithmus"
            algo_2 = "MTD-f"
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
                iteration_count_alg1_list[str(move_count)] = iteration_count_alg1
            else:
                best_move, iteration_count_alg2 = iterative_deepening_mtdf(game, max_depth=5, alpha_beta_player=game.current_player, time_limit=time_limit)
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
    
    def play_game_mtdf_ab(game, time_limit = 60):
        time_limit = time_limit
        # abwechselnd ab3 und mtdf random welcher spieler 1 und 2
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
            algo_1 = "MTD-f"
            algo_2 = "Alpha Beta Algorithmus"
            if game.current_player == 1:
                best_move, iteration_count_alg1 = iterative_deepening_mtdf(game, max_depth=5, alpha_beta_player=game.current_player, time_limit=time_limit)
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

        #winner = 2 if game.current_player == 1 else 1
        return move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit
    
    # Funktion zum Speichern der Spiele in einer JSON-Datei
    def save_game_stats(game_count, move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit, filename='game_stats.json'):
        filename_final = os.path.join(r"C:\Users\Timmy\Desktop\AB MTDF", filename)
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


    ################## ab VS AB 60 SEC ##################
    def ab_mtdf_60():
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
            
            # ab VS mtdf
            move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit = play_game_ab_mtdf(game)

            # Speichere die Statistiken in einer JSON-Datei
            save_game_stats(game_count, move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit, filename='game_ab_mtdf_60.json')

            game_count += 1

            # Testweise nur eine bestimmte Anzahl Spiele spielen
            if game_count > 25:  # Beispiel: Stoppe nach 5 Spielen
                break

            time.sleep(time_limit)
        #"""
        #game_count = 2
        while True:
            print(f"Spiel {game_count} beginnt")
            game = AmazonsGame()

            # mtdf VS ab
            move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit = play_game_mtdf_ab(game)

            # Speichere die Statistiken in einer JSON-Datei
            save_game_stats(game_count, move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit, filename='game_ab_mtdf_60.json')

            game_count += 1

            if game_count > 50:  # Beispiel: Stoppe nach 10 Spielen
                break

            time.sleep(time_limit)

    ################## ab VS AB 30 SEC ##################
    def ab_mtdf_30():
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
            
            # ab VS AB
            move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit = play_game_ab_mtdf(game, time_limit=30)

            # Speichere die Statistiken in einer JSON-Datei
            save_game_stats(game_count, move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit, filename='game_ab_mtdf_30.json')

            game_count += 1

            # Testweise nur eine bestimmte Anzahl Spiele spielen
            if game_count > 25:  # Beispiel: Stoppe nach 5 Spielen
                break

            time.sleep(time_limit)
        #"""
        #game_count = 8
        while True:
            print(f"Spiel {game_count} beginnt")
            game = AmazonsGame()

            # PVS VS ab
            move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit = play_game_mtdf_ab(game, time_limit=30)

            # Speichere die Statistiken in einer JSON-Datei
            save_game_stats(game_count, move_count, move_stats_alg1, move_stats_alg2, iteration_count_alg1_list, iteration_count_alg2_list, winner, algo_1, algo_2, time_limit, filename='game_ab_mtdf_30.json')

            game_count += 1

            if game_count > 50:  # Beispiel: Stoppe nach 10 Spielen
                break

            time.sleep(time_limit)

    #ab_mtdf_60()
    #ab_mtdf_30()




    ############################################################### TESTING #################################################################
    #"""
    game = AmazonsGame()

    # Frühe Spielphase (Nach 10 Zügen)
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 'X', 0, 1, 0, 'X'], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 'X', 0, 0, 2, 0, 'X', 0], [0, 0, 0, 2, 0, 'X', 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 'X', 0, 0, 'X', 0, 1, 0, 0, 0], [0, 0, 'X', 1, 0, 2, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 'X', 0, 0], [0, 0, 0, 0, 'X', 0, 0, 0, 0, 0]]
    
    # Mittlere Spielphase (Nach 30 Zügen)
    #board = [[0, 0, 0, 'X', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 'X', 'X', 0, 0, 'X'], [0, 0, 1, 'X', 0, 'X', 2, 'X', 0, 0], [0, 0, 2, 'X', 0, 1, 0, 'X', 'X', 0], [0, 0, 0, 'X', 0, 'X', 0, 0, 0, 0], [0, 0, 0, 0, 0, 'X', 0, 'X', 'X', 0], [0, 'X', 0, 1, 'X', 0, 'X', 0, 'X', 0], ['X', 'X', 'X', 0, 0, 'X', 0, 2, 1, 0], [0, 'X', 0, 'X', 'X', 0, 0, 'X', 0, 0], [0, 2, 0, 'X', 'X', 0, 0, 0, 0, 'X']]
    
    # End-Spielphase (Nach 50 Zügen)
    #board = [[0, 0, 0, 'X', 0, 0, 0, 'X', 2, 'X'], [0, 0, 0, 0, 1, 'X', 'X', 'X', 1, 'X'], ['X', 'X', 'X', 'X', 0, 'X', 0, 'X', 0, 0], [2, 0, 'X', 'X', 0, 0, 0, 'X', 'X', 0], [0, 'X', 'X', 'X', 0, 'X', 0, 'X', 0, 0], ['X', 0, 0, 0, 'X', 'X', 0, 'X', 'X', 0], ['X', 'X', 'X', 0, 'X', 0, 'X', 0, 'X', 0], ['X', 'X', 'X', 'X', 0, 'X', 'X', 'X', 0, 1], [2, 'X', 0, 'X', 'X', 1, 0, 'X', 0, 0], ['X', 0, 0, 'X', 'X', 2, 'X', 'X', 0, 'X']]

    game.board = board
    
    self_amazons = {1: [], 2: []}
    for x, row in enumerate(board):
        for y, value in enumerate(row):
            if value == 1:
                self_amazons[1].append((x, y))
            elif value == 2:
                self_amazons[2].append((x, y))

    game.amazons = self_amazons
    game.current_player = 1

    print(f"Ausgangs-Eval: {game.evaluate_position()}")

    for i in range(20):

        print(f"Test Nummer {i+1}")

        ######## MCTS ########
        simulation_game_1 = game.copy()
        best_move, iteration_count = mcts3(game, is_to_move=game.current_player, time_limit=60)
        simulation_game_1.make_move(*best_move)
        print(f"MCTS - Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_1.evaluate_position()}")

        ######## Alpha Beta ########
        simulation_game_2 = game.copy()
        best_move, iteration_count = iterative_deepening(game, 5, alpha_beta_player=game.current_player, time_limit=60)
        simulation_game_2.make_move(*best_move)
        print(f"Alpha Beta - Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_2.evaluate_position()}")

        ######## PVS ########
        simulation_game_3 = game.copy()
        best_move, iteration_count = iterative_deepening_pvs(game, 5, alpha_beta_player=game.current_player, time_limit=60)
        simulation_game_3.make_move(*best_move)
        print(f"PVS - Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_3.evaluate_position()}")

        ######## MTD-f ########
        simulation_game_4 = game.copy()
        best_move, iteration_count = iterative_deepening_mtdf(game, 5, alpha_beta_player=game.current_player, time_limit=60)
        simulation_game_4.make_move(*best_move)
        print(f"MTD-f - Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_4.evaluate_position()}")#

    #"""
    print("----------------------------------------------------------------")

    game = AmazonsGame()

    # Frühe Spielphase (Nach 10 Zügen)
    #board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 'X', 0, 1, 0, 'X'], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 'X', 0, 0, 2, 0, 'X', 0], [0, 0, 0, 2, 0, 'X', 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 'X', 0, 0, 'X', 0, 1, 0, 0, 0], [0, 0, 'X', 1, 0, 2, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 'X', 0, 0], [0, 0, 0, 0, 'X', 0, 0, 0, 0, 0]]
    
    # Mittlere Spielphase (Nach 30 Zügen)
    board = [[0, 0, 0, 'X', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 'X', 'X', 0, 0, 'X'], [0, 0, 1, 'X', 0, 'X', 2, 'X', 0, 0], [0, 0, 2, 'X', 0, 1, 0, 'X', 'X', 0], [0, 0, 0, 'X', 0, 'X', 0, 0, 0, 0], [0, 0, 0, 0, 0, 'X', 0, 'X', 'X', 0], [0, 'X', 0, 1, 'X', 0, 'X', 0, 'X', 0], ['X', 'X', 'X', 0, 0, 'X', 0, 2, 1, 0], [0, 'X', 0, 'X', 'X', 0, 0, 'X', 0, 0], [0, 2, 0, 'X', 'X', 0, 0, 0, 0, 'X']]
    
    # End-Spielphase (Nach 50 Zügen)
    #board = [[0, 0, 0, 'X', 0, 0, 0, 'X', 2, 'X'], [0, 0, 0, 0, 1, 'X', 'X', 'X', 1, 'X'], ['X', 'X', 'X', 'X', 0, 'X', 0, 'X', 0, 0], [2, 0, 'X', 'X', 0, 0, 0, 'X', 'X', 0], [0, 'X', 'X', 'X', 0, 'X', 0, 'X', 0, 0], ['X', 0, 0, 0, 'X', 'X', 0, 'X', 'X', 0], ['X', 'X', 'X', 0, 'X', 0, 'X', 0, 'X', 0], ['X', 'X', 'X', 'X', 0, 'X', 'X', 'X', 0, 1], [2, 'X', 0, 'X', 'X', 1, 0, 'X', 0, 0], ['X', 0, 0, 'X', 'X', 2, 'X', 'X', 0, 'X']]

    game.board = board
    
    self_amazons = {1: [], 2: []}
    for x, row in enumerate(board):
        for y, value in enumerate(row):
            if value == 1:
                self_amazons[1].append((x, y))
            elif value == 2:
                self_amazons[2].append((x, y))

    game.amazons = self_amazons
    game.current_player = 1

    print(f"Ausgangs-Eval: {game.evaluate_position()}")

    for i in range(20):

        print(f"Test Nummer {i+1}")

        ######## MCTS ########
        simulation_game_1 = game.copy()
        best_move, iteration_count = mcts3(game, is_to_move=game.current_player, time_limit=60)
        simulation_game_1.make_move(*best_move)
        print(f"MCTS - Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_1.evaluate_position()}")

        ######## Alpha Beta ########
        simulation_game_2 = game.copy()
        best_move, iteration_count = iterative_deepening(game, 5, alpha_beta_player=game.current_player, time_limit=60)
        simulation_game_2.make_move(*best_move)
        print(f"Alpha Beta - Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_2.evaluate_position()}")

        ######## PVS ########
        simulation_game_3 = game.copy()
        best_move, iteration_count = iterative_deepening_pvs(game, 5, alpha_beta_player=game.current_player, time_limit=60)
        simulation_game_3.make_move(*best_move)
        print(f"PVS - Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_3.evaluate_position()}")

        ######## MTD-f ########
        simulation_game_4 = game.copy()
        best_move, iteration_count = iterative_deepening_mtdf(game, 5, alpha_beta_player=game.current_player, time_limit=60)
        simulation_game_4.make_move(*best_move)
        print(f"MTD-f - Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_4.evaluate_position()}")#

    print("----------------------------------------------------------------")

    game = AmazonsGame()

    # Frühe Spielphase (Nach 10 Zügen)
    #board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 'X', 0, 1, 0, 'X'], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 'X', 0, 0, 2, 0, 'X', 0], [0, 0, 0, 2, 0, 'X', 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 'X', 0, 0, 'X', 0, 1, 0, 0, 0], [0, 0, 'X', 1, 0, 2, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 'X', 0, 0], [0, 0, 0, 0, 'X', 0, 0, 0, 0, 0]]
    
    # Mittlere Spielphase (Nach 30 Zügen)
    #board = [[0, 0, 0, 'X', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 'X', 'X', 0, 0, 'X'], [0, 0, 1, 'X', 0, 'X', 2, 'X', 0, 0], [0, 0, 2, 'X', 0, 1, 0, 'X', 'X', 0], [0, 0, 0, 'X', 0, 'X', 0, 0, 0, 0], [0, 0, 0, 0, 0, 'X', 0, 'X', 'X', 0], [0, 'X', 0, 1, 'X', 0, 'X', 0, 'X', 0], ['X', 'X', 'X', 0, 0, 'X', 0, 2, 1, 0], [0, 'X', 0, 'X', 'X', 0, 0, 'X', 0, 0], [0, 2, 0, 'X', 'X', 0, 0, 0, 0, 'X']]
    
    # End-Spielphase (Nach 50 Zügen)
    board = [[0, 0, 0, 'X', 0, 0, 0, 'X', 2, 'X'], [0, 0, 0, 0, 1, 'X', 'X', 'X', 1, 'X'], ['X', 'X', 'X', 'X', 0, 'X', 0, 'X', 0, 0], [2, 0, 'X', 'X', 0, 0, 0, 'X', 'X', 0], [0, 'X', 'X', 'X', 0, 'X', 0, 'X', 0, 0], ['X', 0, 0, 0, 'X', 'X', 0, 'X', 'X', 0], ['X', 'X', 'X', 0, 'X', 0, 'X', 0, 'X', 0], ['X', 'X', 'X', 'X', 0, 'X', 'X', 'X', 0, 1], [2, 'X', 0, 'X', 'X', 1, 0, 'X', 0, 0], ['X', 0, 0, 'X', 'X', 2, 'X', 'X', 0, 'X']]

    game.board = board
    
    self_amazons = {1: [], 2: []}
    for x, row in enumerate(board):
        for y, value in enumerate(row):
            if value == 1:
                self_amazons[1].append((x, y))
            elif value == 2:
                self_amazons[2].append((x, y))

    game.amazons = self_amazons
    game.current_player = 1

    print(f"Ausgangs-Eval: {game.evaluate_position()}")

    for i in range(20):

        print(f"Test Nummer {i+1}")

        ######## MCTS ########
        simulation_game_1 = game.copy()
        best_move, iteration_count = mcts3(game, is_to_move=game.current_player, time_limit=60)
        simulation_game_1.make_move(*best_move)
        print(f"MCTS - Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_1.evaluate_position()}")

        ######## Alpha Beta ########
        simulation_game_2 = game.copy()
        best_move, iteration_count = iterative_deepening(game, 5, alpha_beta_player=game.current_player, time_limit=60)
        simulation_game_2.make_move(*best_move)
        print(f"Alpha Beta - Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_2.evaluate_position()}")

        ######## PVS ########
        simulation_game_3 = game.copy()
        best_move, iteration_count = iterative_deepening_pvs(game, 5, alpha_beta_player=game.current_player, time_limit=60)
        simulation_game_3.make_move(*best_move)
        print(f"PVS - Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_3.evaluate_position()}")

        ######## MTD-f ########
        simulation_game_4 = game.copy()
        best_move, iteration_count = iterative_deepening_mtdf(game, 5, alpha_beta_player=game.current_player, time_limit=60)
        simulation_game_4.make_move(*best_move)
        print(f"MTD-f - Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_4.evaluate_position()}")