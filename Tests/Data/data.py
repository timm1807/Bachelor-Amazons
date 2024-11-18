import re
from collections import defaultdict

data = """
Test Nummer 1
MCTS - Zug: ((1, 4), (1, 3), (0, 2)) | Iteration Count: 667 | Eval of this Move: 26.901807291666664
Alpha Beta - Zug: ((8, 5), (5, 2), (8, 5)) | Iteration Count: 33642 | Eval of this Move: 27.983442708333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 52068 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((8, 5), (7, 4), (6, 3)) | Iteration Count: 34075 | Eval of this Move: 23.56565625
Test Nummer 2
MCTS - Zug: ((8, 5), (5, 2), (8, 5)) | Iteration Count: 732 | Eval of this Move: 27.983442708333335
Alpha Beta - Zug: ((8, 5), (5, 2), (8, 5)) | Iteration Count: 34039 | Eval of this Move: 27.983442708333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 53639 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((7, 9), (8, 9), (7, 8)) | Iteration Count: 45342 | Eval of this Move: 25.7987578125
Test Nummer 3
MCTS - Zug: ((8, 5), (7, 4), (8, 5)) | Iteration Count: 770 | Eval of this Move: 26.58382291666667
Alpha Beta - Zug: ((8, 5), (6, 3), (8, 5)) | Iteration Count: 45404 | Eval of this Move: 26.599286458333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 53130 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((1, 4), (2, 4), (0, 2)) | Iteration Count: 45561 | Eval of this Move: 24.575526041666667
Test Nummer 4
MCTS - Zug: ((7, 9), (8, 9), (5, 6)) | Iteration Count: 680 | Eval of this Move: 27.990091145833333
Alpha Beta - Zug: ((8, 5), (6, 3), (8, 5)) | Iteration Count: 47631 | Eval of this Move: 26.599286458333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 53790 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((7, 9), (8, 9), (7, 8)) | Iteration Count: 44407 | Eval of this Move: 25.7987578125
Test Nummer 5
MCTS - Zug: ((1, 4), (1, 3), (0, 2)) | Iteration Count: 694 | Eval of this Move: 26.901807291666664
Alpha Beta - Zug: ((8, 5), (6, 3), (8, 5)) | Iteration Count: 48785 | Eval of this Move: 26.599286458333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 53002 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((7, 9), (7, 8), (5, 6)) | Iteration Count: 38293 | Eval of this Move: 24.288778645833332
Test Nummer 6
MCTS - Zug: ((7, 9), (8, 9), (3, 9)) | Iteration Count: 669 | Eval of this Move: 26.894424479166666
Alpha Beta - Zug: ((8, 5), (6, 3), (8, 5)) | Iteration Count: 36420 | Eval of this Move: 26.599286458333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 52624 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((7, 9), (8, 9), (7, 8)) | Iteration Count: 45484 | Eval of this Move: 25.7987578125
Test Nummer 7
MCTS - Zug: ((7, 9), (8, 9), (9, 8)) | Iteration Count: 713 | Eval of this Move: 27.894424479166666
Alpha Beta - Zug: ((8, 5), (6, 3), (8, 5)) | Iteration Count: 46083 | Eval of this Move: 26.599286458333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 52170 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((1, 4), (0, 4), (1, 4)) | Iteration Count: 33054 | Eval of this Move: 18.164333333333335
Test Nummer 8
MCTS - Zug: ((8, 5), (7, 4), (5, 6)) | Iteration Count: 694 | Eval of this Move: 25.412989583333335
Alpha Beta - Zug: ((8, 5), (5, 2), (8, 5)) | Iteration Count: 33226 | Eval of this Move: 27.983442708333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 51844 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((7, 9), (8, 9), (7, 8)) | Iteration Count: 35378 | Eval of this Move: 25.7987578125
Test Nummer 9
MCTS - Zug: ((1, 4), (2, 4), (4, 4)) | Iteration Count: 693 | Eval of this Move: 24.958192708333332
Alpha Beta - Zug: ((8, 5), (5, 2), (8, 5)) | Iteration Count: 34617 | Eval of this Move: 27.983442708333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 51286 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((1, 4), (1, 3), (3, 5)) | Iteration Count: 33363 | Eval of this Move: 25.997473958333334
Test Nummer 10
MCTS - Zug: ((7, 9), (8, 9), (2, 9)) | Iteration Count: 683 | Eval of this Move: 26.894424479166666
Alpha Beta - Zug: ((8, 5), (5, 2), (8, 5)) | Iteration Count: 33497 | Eval of this Move: 27.983442708333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 51080 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((8, 5), (7, 4), (6, 3)) | Iteration Count: 34007 | Eval of this Move: 23.56565625
Test Nummer 11
MCTS - Zug: ((1, 4), (2, 4), (4, 4)) | Iteration Count: 701 | Eval of this Move: 24.958192708333332
Alpha Beta - Zug: ((8, 5), (5, 2), (8, 5)) | Iteration Count: 34221 | Eval of this Move: 27.983442708333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 53822 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 36012 | Eval of this Move: 23.95627604166667
Test Nummer 12
MCTS - Zug: ((1, 4), (1, 3), (0, 4)) | Iteration Count: 689 | Eval of this Move: 26.901807291666664
Alpha Beta - Zug: ((8, 5), (6, 3), (8, 5)) | Iteration Count: 33622 | Eval of this Move: 26.599286458333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 52495 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((1, 4), (1, 3), (0, 2)) | Iteration Count: 33119 | Eval of this Move: 26.901807291666664
Test Nummer 13
MCTS - Zug: ((1, 4), (1, 3), (3, 5)) | Iteration Count: 682 | Eval of this Move: 25.997473958333334
Alpha Beta - Zug: ((8, 5), (5, 2), (8, 5)) | Iteration Count: 33149 | Eval of this Move: 27.983442708333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 51722 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((7, 9), (7, 8), (5, 6)) | Iteration Count: 33299 | Eval of this Move: 24.288778645833332
Test Nummer 14
MCTS - Zug: ((7, 9), (8, 9), (8, 8)) | Iteration Count: 671 | Eval of this Move: 27.894424479166666
Alpha Beta - Zug: ((8, 5), (5, 2), (8, 5)) | Iteration Count: 33322 | Eval of this Move: 27.983442708333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 52432 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((7, 9), (7, 8), (5, 6)) | Iteration Count: 44172 | Eval of this Move: 24.288778645833332
Test Nummer 15
MCTS - Zug: ((7, 9), (8, 9), (6, 7)) | Iteration Count: 723 | Eval of this Move: 26.894424479166666
Alpha Beta - Zug: ((8, 5), (6, 3), (8, 5)) | Iteration Count: 47217 | Eval of this Move: 26.599286458333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 52458 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((7, 9), (7, 8), (5, 6)) | Iteration Count: 33100 | Eval of this Move: 24.288778645833332
Test Nummer 16
MCTS - Zug: ((7, 9), (8, 9), (7, 8)) | Iteration Count: 708 | Eval of this Move: 25.7987578125
Alpha Beta - Zug: ((8, 5), (5, 2), (8, 5)) | Iteration Count: 32960 | Eval of this Move: 27.983442708333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 49690 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((1, 4), (2, 4), (0, 2)) | Iteration Count: 33845 | Eval of this Move: 24.575526041666667
Test Nummer 17
MCTS - Zug: ((1, 4), (1, 3), (0, 4)) | Iteration Count: 681 | Eval of this Move: 26.901807291666664
Alpha Beta - Zug: ((8, 5), (5, 2), (8, 5)) | Iteration Count: 33312 | Eval of this Move: 27.983442708333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 50674 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((8, 5), (6, 3), (7, 4)) | Iteration Count: 33339 | Eval of this Move: 23.731453125
Test Nummer 18
MCTS - Zug: ((1, 4), (1, 3), (0, 2)) | Iteration Count: 700 | Eval of this Move: 26.901807291666664
Alpha Beta - Zug: ((8, 5), (5, 2), (8, 5)) | Iteration Count: 32782 | Eval of this Move: 27.983442708333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 49076 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((7, 9), (7, 8), (9, 8)) | Iteration Count: 42515 | Eval of this Move: 24.240945312500003
Test Nummer 19
MCTS - Zug: ((7, 9), (8, 9), (5, 6)) | Iteration Count: 636 | Eval of this Move: 27.990091145833333
Alpha Beta - Zug: ((8, 5), (6, 3), (8, 5)) | Iteration Count: 40451 | Eval of this Move: 26.599286458333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 51241 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((1, 4), (2, 4), (0, 2)) | Iteration Count: 45404 | Eval of this Move: 24.575526041666667
Test Nummer 20
MCTS - Zug: ((1, 4), (1, 3), (1, 4)) | Iteration Count: 725 | Eval of this Move: 26.901807291666664
Alpha Beta - Zug: ((8, 5), (6, 3), (8, 5)) | Iteration Count: 46577 | Eval of this Move: 26.599286458333335
PVS - Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 52984 | Eval of this Move: 23.95627604166667
MTD-f - Zug: ((7, 9), (8, 9), (7, 8)) | Iteration Count: 44237 | Eval of this Move: 25.7987578125
"""

iteration_counts = defaultdict(list)
evals = defaultdict(list)

# Regex
pattern = r"(\w+) - Zug: .*? \| Iteration Count: (\d+) \| Eval of this Move: ([\d.]+)"

# Durchlaufen der Zeilen und Hinzufügen zu den Dictionaries
for match in re.finditer(pattern, data):
    algo = match.group(1)
    iteration_count = int(match.group(2))
    eval_of_move = float(match.group(3))

    iteration_counts[algo].append(iteration_count)
    evals[algo].append(eval_of_move)

for algo in iteration_counts:
    avg_iteration_count = sum(iteration_counts[algo]) / len(iteration_counts[algo])
    avg_eval = sum(evals[algo]) / len(evals[algo])

    print(f"{algo}:")
    print(f"Durchschnittlicher Iteration Count: {avg_iteration_count}")
    print(f"Durchschnittlicher Eval of this Move: {avg_eval}")
    print()