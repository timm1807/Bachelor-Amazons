import re
import pandas as pd

data = """
Test Nummer 1
MCTS - Tiefe: 4 | Zug: ((7, 9), (8, 9), (8, 8)) | Iteration Count: 121 | Eval of this Move: 27.894424479166666 | Zeit: 12.446443319320679
Alpha Beta - Tiefe: 4 | Zug: ((8, 5), (6, 3), (8, 5)) | Iteration Count: 104044 | Eval of this Move: 26.599286458333335 | Zeit: 146.43233180046082
PVS - Tiefe: 4 | Zug: ((8, 5), (5, 2), (5, 1)) | Iteration Count: 77416 | Eval of this Move: 23.95627604166667 | Zeit: 73.75348949432373
MTD-f - Tiefe: 4 | Zug: ((8, 5), (6, 3), (5, 3)) | Iteration Count: 77105 | Eval of this Move: 24.444453125 | Zeit: 109.29360508918762
"""

# Regex
pattern = r"(\w+(?: \w+)*) - Tiefe: \d+ \| Zug: \(.+\) \| Iteration Count: (\d+) \| Eval of this Move: ([\d.]+) \| Zeit: ([\d.]+)"

records = re.findall(pattern, data)
df = pd.DataFrame(records, columns=["Algorithm", "Iteration Count", "Eval of this Move", "Zeit"])

df["Iteration Count"] = pd.to_numeric(df["Iteration Count"])
df["Eval of this Move"] = pd.to_numeric(df["Eval of this Move"])
df["Zeit"] = pd.to_numeric(df["Zeit"])

# Durchschnittswerte
avg_df = df.groupby("Algorithm").mean()
avg_df["Zeit"] = avg_df["Zeit"].round(4)

print(avg_df)
