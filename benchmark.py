from minimax_agent import MinimaxAgent
from alphabeta_agent import AlphaBetaAgent
from expectimax_agent import ExpectimaxAgent
from game import GameState
from metrics import METRICS
import statistics as stats
import csv
import time

def run_one_game(agentX, agentO, depth):
    METRICS.reset()
    s = GameState()
    agents = {'X': (agentX, depth), 'O': (agentO, depth)}

    while not s.is_terminal():
        agent, d = agents[s.to_move]
        move = agent.get_action(s, d)
        s = s.generate_successor(move)

    return (
        s.utility(),  # +1, 0, -1
        sum(METRICS.move_times),
        METRICS.node_counts.get("expectimax", 0),
        METRICS.node_counts.get("minimax", 0),
        METRICS.node_counts.get("alphabeta", 0),
        METRICS.prune_counts.get("alphabeta", 0)
    )


def benchmark(runs=3, depths=(None, 3, 5), csv_file="results_tictactoe.csv"):
    agent_types = [
        ("ExpectimaxAgent", ExpectimaxAgent),
        ("MinimaxAgent", MinimaxAgent),
        ("AlphaBetaAgent", AlphaBetaAgent),
    ]

    matchups = []
    for X_name, X_cls in agent_types:
        for O_name, O_cls in agent_types:
            matchups.append((X_name, X_cls, O_name, O_cls))

    rows = []

    for labelX, Xc, labelO, Oc in matchups:
        for d in depths:
            results = []
            times, e_nodes, m_nodes, a_nodes, prunes = [], [], [], [], []
            for _ in range(runs):
                r, t, e, m, a, p = run_one_game(Xc(), Oc(), d)
                results.append(r)
                times.append(t)
                e_nodes.append(e)
                m_nodes.append(m)
                a_nodes.append(a)
                prunes.append(p)

            rows.append({
                "PlayerX": labelX,
                "PlayerO": labelO,
                "Depth": "Full" if d is None else d,
                "Games": runs,
                "Wins(X)": results.count(1),
                "Draws": results.count(0),
                "Wins(O)": results.count(-1),
                "AvgTime": round(stats.mean(times), 4),
                "AvgNodes_Expectimax": round(stats.mean(e_nodes), 2),
                "AvgNodes_Minimax": round(stats.mean(m_nodes), 2),
                "AvgNodes_AlphaBeta": round(stats.mean(a_nodes), 2),
                "AvgPrunes_AlphaBeta": round(stats.mean(prunes), 2),
            })

    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("done")

if __name__ == "__main__":
    print(">>> Starting full benchmark...")
    benchmark(runs=3, depths=(None, 3, 5), csv_file="results_tictactoe.csv")
    print(">>> Finished")
