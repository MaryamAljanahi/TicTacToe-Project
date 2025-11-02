# make_figs_simple.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

csv_path = Path("results_tictactoe.csv")
if not csv_path.exists():
    raise SystemExit("ERROR: results_tictactoe.csv not found.")

df = pd.read_csv(csv_path)

# Normalize naming
rename_map = {
    "ExpectimaxAgent": "Expectimax",
    "MinimaxAgent": "Minimax",
    "AlphaBetaAgent": "Alpha-Beta"
}
df["PlayerX"] = df["PlayerX"].map(rename_map)
df["PlayerO"] = df["PlayerO"].map(rename_map)

# ---------------- Overall Win Counts ----------------
wins = {
    "Expectimax": df[(df["PlayerX"] == "Expectimax")]["Wins(X)"].sum() +
                  df[(df["PlayerO"] == "Expectimax")]["Wins(O)"].sum(),
    "Minimax": df[(df["PlayerX"] == "Minimax")]["Wins(X)"].sum() +
               df[(df["PlayerO"] == "Minimax")]["Wins(O)"].sum(),
    "Alpha-Beta": df[(df["PlayerX"] == "Alpha-Beta")]["Wins(X)"].sum() +
                   df[(df["PlayerO"] == "Alpha-Beta")]["Wins(O)"].sum()
}

plt.figure(figsize=(7,5))
plt.bar(wins.keys(), wins.values())
plt.ylabel("Total Wins")
plt.title("Total Wins by Algorithm")
plt.tight_layout()
plt.savefig("chart_wins.png", dpi=200)
plt.close()

# ---------------- Average Node Expansion ----------------
# Weighted by number of games each appears in
node_data = {
    "Expectimax": df["AvgNodes_Expectimax"].mean(),
    "Minimax": df["AvgNodes_Minimax"].mean(),
    "Alpha-Beta": df["AvgNodes_AlphaBeta"].mean()
}

plt.figure(figsize=(7,5))
plt.bar(node_data.keys(), node_data.values())
plt.ylabel("Avg Nodes Expanded")
plt.title("Search Efficiency (Lower is Better)")
plt.tight_layout()
plt.savefig("chart_nodes.png", dpi=200)
plt.close()

