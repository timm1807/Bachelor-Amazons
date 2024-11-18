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

    ############################################################### TESTING #################################################################

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

    depth = 5
    timelim = 1000000

    for i in range(1):

        print(f"Test Nummer {i+1}")

        ######## MCTS ########
        simulation_game_1 = game.copy()
        start = time.time()
        best_move, iteration_count = mcts3(game, max_depth=depth, is_to_move=game.current_player, time_limit=timelim)
        end = time.time()
        simulation_game_1.make_move(*best_move)
        print(f"MCTS - Tiefe: {depth} | Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_1.evaluate_position()} | Zeit: {end-start}")

        ######## Alpha Beta ########
        simulation_game_2 = game.copy()
        start = time.time()
        best_move, iteration_count = iterative_deepening(game, depth, alpha_beta_player=game.current_player, time_limit=timelim)
        end = time.time()
        simulation_game_2.make_move(*best_move)
        print(f"Alpha Beta - Tiefe: {depth} | Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_2.evaluate_position()} | Zeit: {end-start}")

        ######## PVS ########
        simulation_game_3 = game.copy()
        start = time.time()
        best_move, iteration_count = iterative_deepening_pvs(game, depth, alpha_beta_player=game.current_player, time_limit=timelim)
        end = time.time()
        simulation_game_3.make_move(*best_move)
        print(f"PVS - Tiefe: {depth} | Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_3.evaluate_position()} | Zeit: {end-start}")

        ######## MTD-f ########
        simulation_game_4 = game.copy()
        start = time.time()
        best_move, iteration_count = iterative_deepening_mtdf(game, depth, alpha_beta_player=game.current_player, time_limit=timelim)
        end = time.time()
        simulation_game_4.make_move(*best_move)
        print(f"MTD-f - Tiefe: {depth} | Zug: {best_move} | Iteration Count: {iteration_count} | Eval of this Move: {simulation_game_4.evaluate_position()} | Zeit: {end-start}")