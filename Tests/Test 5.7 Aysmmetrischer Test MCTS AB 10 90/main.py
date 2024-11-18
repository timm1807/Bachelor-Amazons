from alpha_beta import iterative_deepening
from amazons_engine import AmazonsGame
from mcts3 import mcts3
import random
import time

import json
import os

if __name__ == "__main__":

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
                best_move, iteration_count_alg1 = mcts3(game, is_to_move=game.current_player, time_limit=90)
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
                best_move, iteration_count_alg2 = iterative_deepening(game, max_depth=5, alpha_beta_player=game.current_player, time_limit=10)
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
                best_move, iteration_count_alg1 = iterative_deepening(game, max_depth=5, alpha_beta_player=game.current_player, time_limit=10)
                print(best_move)
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
                best_move, iteration_count_alg2 = mcts3(game, is_to_move=game.current_player, time_limit=90)
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
        filename_final = os.path.join(r"C:\Users\Timmy\Desktop\Test 5.7 Aysmmetrischer Test MCTS AB 10 90", filename)
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
            if game_count > 10:  # Beispiel: Stoppe nach 5 Spielen
                break

            time.sleep(90)
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

            if game_count > 20:  # Beispiel: Stoppe nach 10 Spielen
                break

            time.sleep(90)

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
        #game_count = 8
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