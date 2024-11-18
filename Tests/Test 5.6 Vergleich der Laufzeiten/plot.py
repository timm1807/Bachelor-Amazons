import matplotlib.pyplot as plt

algorithms = ['Alpha-Beta', 'Monte-Carlo Tree Search', 'MTD(f)', 'PVS']
depths = ['Tiefe 1', 'Tiefe 2', 'Tiefe 3', 'Tiefe 4']
times = [
    [0.2669, 1.1518, 88.2807, 146.4323],  # Alpha-Beta
    [3.0083, 6.6916, 9.6342, 12.4464],     # MCTS
    [0.5230, 1.2275, 31.5056, 109.2936],  # MTD(f)
    [0.2751, 30.7017, 49.8422, 73.7535]  # PVS
]

plt.figure(figsize=(10, 6))
for i, algo in enumerate(algorithms):
    plt.plot(depths, times[i], marker='o', label=algo)

plt.title("Vergleich der durchschnittlichen Laufzeiten der Algorithmen pro Tiefe", fontsize=15)
plt.xlabel("Tiefe", fontsize=14)
plt.ylabel("Durchschnittliche Laufzeit (Sekunden)", fontsize=14)
plt.legend(title="Algorithmus", fontsize=13)
plt.grid(True)
plt.tight_layout()
plt.show()
