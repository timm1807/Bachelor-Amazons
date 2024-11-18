import json
import glob
import os
import matplotlib.pyplot as plt

output_dir = "average_iterations"
os.makedirs(output_dir, exist_ok=True)

input_files = glob.glob("data*.json")
if not input_files:
    raise FileNotFoundError("No JSON files found")

for input_file in input_files:
    with open(input_file, 'r') as file:
        data = json.load(file)

    move_iterations = {}

    # Durchschnittsiterationen pro zug
    for game_key, game_data in data["average_iterations_per_move"].items():
        for move, iterations in game_data.items():
            if move not in move_iterations:
                move_iterations[move] = []
            move_iterations[move].append(float(iterations))

    average_iterations_per_move = {
        move: round(sum(iterations) / len(iterations), 2) for move, iterations in move_iterations.items()
    }

    output_data = {"average_iterations_per_move": average_iterations_per_move}

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, f"{base_name}.average_iterations_output.json")
    
    with open(output_file, 'w') as outfile:
        json.dump(output_data, outfile, indent=4)

    print(f"Average iterations written to '{output_file}'")
    
output_files = glob.glob(os.path.join(output_dir, "*.average_iterations_output.json"))
data_sources = {}

for file in output_files:
    with open(file, 'r') as f:
        data = json.load(f)
        data_sources[file] = {
            int(move.split()[1]): iterations for move, iterations in data["average_iterations_per_move"].items()
        }

# mapping
file_label_mapping = {
    "dataMCTS.json": "Monte-Carlo Tree Search",
    "dataAB.json": "Alpha-Beta",
    "dataMTDF.json": "MTD(f)",
    "dataPVS.json": "PVS"
}

# Plotting
plt.figure(figsize=(12, 8))
for file, move_data in data_sources.items():
    sorted_moves = sorted(move_data.items())
    moves, iterations = zip(*sorted_moves)
    
    base_name = os.path.basename(file).replace(".average_iterations_output.json", "") + ".json"
    label = file_label_mapping.get(base_name, base_name)
    plt.plot(moves, iterations, marker='o', label=label)

# Plot
plt.title("Durchschnittliche Iterationen pro Zug", fontsize=15)
plt.xlabel("Zugnummer", fontsize=14)
plt.ylabel("Durchschnittliche Iterationen", fontsize=14)
plt.legend(title="Algorithmen", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=13)
plt.grid(True)
plt.tight_layout()
plt.show()
