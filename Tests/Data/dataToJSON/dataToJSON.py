import json
from statistics import mean
import glob
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

json_files = glob.glob(os.path.join(current_dir, "*.json"))
if not json_files:
    raise FileNotFoundError("No JSON file found")

json_file = json_files[0]
print(f"Reading data from: {json_file}")

with open(json_file, 'r') as file:
    data = json.load(file)

first_game_key = next(iter(data)) 
alg_1 = data[first_game_key]['player_1']  # Algorithm used by player_1
alg_2 = data[first_game_key]['player_2']  # Algorithm used by player_2

# store total games, wins, move counts, and eval values
total_games = len(data)
wins_alg1, wins_alg2 = 0, 0
total_move_count = []

# Average evals per game for both ranges (1-5 and 6-10) for alg_1 and alg_2
avg_evals_per_game_1_5_alg1, avg_evals_per_game_6_10_alg1 = [], []
avg_evals_per_game_1_5_alg2, avg_evals_per_game_6_10_alg2 = [], []

iteration_counts_per_move_alg1, iteration_counts_per_move_alg2 = {}, {}

for game_key, game_data in data.items():
    game_number = game_data['game_count']

    # Determine if alg_1 and alg_2 are in player_1 or player_2 position based on the first game
    if game_data['player_1'] == alg_1:
        alg1_iteration_key = 'iteration_count_algo_1'
        alg1_move_stats_key = 'move_stats_alg1'
        alg2_iteration_key = 'iteration_count_algo_2'
        alg2_move_stats_key = 'move_stats_alg2'
    else:
        alg1_iteration_key = 'iteration_count_algo_2'
        alg1_move_stats_key = 'move_stats_alg2'
        alg2_iteration_key = 'iteration_count_algo_1'
        alg2_move_stats_key = 'move_stats_alg1'

    # Calculate win rate 
    winner = game_data['winner']
    if (winner == 1 and game_data['player_1'] == alg_1) or (winner == 2 and game_data['player_2'] == alg_1):
        wins_alg1 += 1
    elif (winner == 1 and game_data['player_1'] == alg_2) or (winner == 2 and game_data['player_2'] == alg_2):
        wins_alg2 += 1

    # Collect move counts
    total_move_count.append(game_data['move_count'])

    # Calculate average evals
    evals_alg1 = [eval for stats in game_data[alg1_move_stats_key].values() for eval in stats['evals']]
    evals_alg2 = [eval for stats in game_data[alg2_move_stats_key].values() for eval in stats['evals']]

    if game_number <= round(total_games/2):
        avg_evals_per_game_1_5_alg1.append(mean(evals_alg1))
        avg_evals_per_game_1_5_alg2.append(mean(evals_alg2))
    else:
        avg_evals_per_game_6_10_alg1.append(mean(evals_alg1))
        avg_evals_per_game_6_10_alg2.append(mean(evals_alg2))

    # Collect iteration counts per move for alg_1
    for move, iterations in game_data[alg1_iteration_key].items():
        if move not in iteration_counts_per_move_alg1:
            iteration_counts_per_move_alg1[move] = []
        iteration_counts_per_move_alg1[move].append(iterations)

    # Collect iteration counts per move for alg_2
    for move, iterations in game_data[alg2_iteration_key].items():
        if move not in iteration_counts_per_move_alg2:
            iteration_counts_per_move_alg2[move] = []
        iteration_counts_per_move_alg2[move].append(iterations)

# Win rate
win_rate_alg1 = wins_alg1 / total_games * 100
win_rate_alg2 = wins_alg2 / total_games * 100

# avg move count
average_move_count = mean(total_move_count)

# average evals
average_evals_1_5_alg1 = mean(avg_evals_per_game_1_5_alg1)
average_evals_1_5_alg2 = mean(avg_evals_per_game_1_5_alg2)
average_evals_6_10_alg1 = mean(avg_evals_per_game_6_10_alg1)
average_evals_6_10_alg2 = mean(avg_evals_per_game_6_10_alg2)

# Average iterations
average_iterations_per_move_alg1 = {move: mean(iterations) for move, iterations in sorted(iteration_counts_per_move_alg1.items(), key=lambda x: int(x[0]))}
average_iterations_per_move_alg2 = {move: mean(iterations) for move, iterations in sorted(iteration_counts_per_move_alg2.items(), key=lambda x: int(x[0]))}

# Display results
print("Win Rate:")
print(f"{alg_1}: {win_rate_alg1}%")
print(f"{alg_2}: {win_rate_alg2}%\n")

print(f"Average Move Count: {average_move_count }")

print("\nAverage Evals per Game (Spiele 1-5):")
print(f"{alg_1} ({'Spieler 1' if alg_1 == data[first_game_key]['player_1'] else 'Spieler 2'}): {average_evals_1_5_alg1}")
print(f"{alg_2} ({'Spieler 1' if alg_2 == data[first_game_key]['player_1'] else 'Spieler 2'}): {average_evals_1_5_alg2}")

print("\nAverage Evals per Game (Spiele 6-10):")
print(f"{alg_1} ({'Spieler 2' if alg_1 == data[first_game_key]['player_1'] else 'Spieler 1'}): {average_evals_6_10_alg1}")
print(f"{alg_2} ({'Spieler 2' if alg_2 == data[first_game_key]['player_1'] else 'Spieler 1'}): {average_evals_6_10_alg2}\n")

print("Average Iterations per Move:")
print(f"{alg_1}:")
for move, avg_iterations in average_iterations_per_move_alg1.items():
    print(f"Move {move}: {avg_iterations}")
print(f"\n{alg_2}:")
for move, avg_iterations in average_iterations_per_move_alg2.items():
    print(f"Move {move}: {avg_iterations}")


# Organize results into a dictionary
results = {
    "win_rate": {
        alg_1: f"{win_rate_alg1}%",
        alg_2: f"{win_rate_alg2}%"
    },
    "average_move_count": f"{average_move_count}",
    "average_evals_per_game": {
        "spiele_1_5": {
            alg_1: f"{average_evals_1_5_alg1}",
            alg_2: f"{average_evals_1_5_alg2}"
        },
        "spiele_6_10": {
            alg_2: f"{average_evals_6_10_alg2}",
            alg_1: f"{average_evals_6_10_alg1}"
        }
    },
    "average_iterations_per_move": {
        alg_1: {f"Move {move}": f"{avg_iterations}" for move, avg_iterations in average_iterations_per_move_alg1.items()},
        alg_2: {f"Move {move}": f"{avg_iterations}" for move, avg_iterations in average_iterations_per_move_alg2.items()}
    }
}

output_file = f"{os.path.splitext(json_file)[0]}_output_results.json"

with open(output_file, "w") as outfile:
    json.dump(results, outfile, indent=4)

print(f"Results written to '{output_file}'")