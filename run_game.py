import argparse
import random
from game import GameState
from minimax_agent import MinimaxAgent
from alphabeta_agent import AlphaBetaAgent
from expectimax_agent import ExpectimaxAgent
from evaluation import betterEvaluationFunction
from metrics import METRICS



# ===============================================================
# STANDARD AGENT vs AGENT PLAY
# ===============================================================
def play_game(agentX, agentO, depth_limit=None, verbose=True):
    """Runs a Tic-Tac-Toe game between two AI agents (X and O)."""
    state = GameState()

    METRICS.reset() #reset for this game
    def display_board(s: GameState):
        board = [c if c is not None else " " for c in s.board]
        print(f"\n   {board[0]} | {board[1]} | {board[2]} ")
        print("  -----------")
        print(f"   {board[3]} | {board[4]} | {board[5]} ")
        print("  -----------")
        print(f"   {board[6]} | {board[7]} | {board[8]} ")
        print("   0   1   2   (cell indices)\n")

    agent_x_name = type(agentX).__name__
    agent_o_name = type(agentO).__name__

    if verbose:
        print("\n" + "=" * 50)
        print("           TIC-TAC-TOE AI BATTLE")
        print("=" * 50)
        print(f"Player X: {agent_x_name}")
        print(f"Player O: {agent_o_name}")
        print(f"Search Depth: {depth_limit if depth_limit else 'Full'}")
        print("\nInitial Board:")
        display_board(state)


    move_num = 1
    while not state.is_terminal():
        current_player = state.to_move
        agent = agentX if current_player == 'X' else agentO
        action = agent.get_action(state, depth_limit)

        if action is None:
            legal = state.get_legal_actions()
            action = random.choice(legal)
            print(f"[WARNING] {type(agent).__name__} returned None - using random move {action}")

        state = state.generate_successor(action)

        if verbose:
            print(f"\n--- MOVE {move_num} ---")
            print(f"{type(agent).__name__} ({current_player}) chooses cell {action}")
            display_board(state)
            move_num += 1

    winner = state.winner()
    print("\n" + "=" * 50)
    print("             GAME RESULTS")
    print("=" * 50)
    if winner is None:
        print("Result: DRAW")
    else:
        print(f"WINNER: {type(agentX).__name__ if winner == 'X' else type(agentO).__name__} ({winner})")
    print("\nFinal Board:")
    display_board(state)

    # ✅ metrics summary
    total_time = sum(METRICS.move_times)
    exp_nodes = METRICS.node_counts.get("expectimax", 0)
    mini_nodes = METRICS.node_counts.get("minimax", 0)
    ab_nodes = METRICS.node_counts.get("alphabeta", 0)
    prunes = METRICS.prune_counts.get("alphabeta", 0)

    print("Metrics:")
    print(f"  Total decision time (s): {total_time:.6f}")
    print(f"  Nodes expanded - Expectimax: {exp_nodes}")
    print(f"  Nodes expanded - Minimax:   {mini_nodes}")
    print(f"  Nodes expanded - AlphaBeta: {ab_nodes}")
    print(f"  AlphaBeta prunes:           {prunes}")
    print("=" * 50)
    print("=" * 50)


# ===============================================================
# HUMAN vs AI MODE (Randomly chooses who starts)
# ===============================================================
def play_human_vs_ai(ai_agent, depth_limit=None):
    """
    Human vs AI mode via command line.
    Randomly chooses who starts first (AI or human).
    """
    state = GameState()
    human_symbol, ai_symbol = ('O', 'X') if random.choice([True, False]) else ('X', 'O')
    print("\n" + "=" * 50)
    print("          HUMAN vs AI TIC-TAC-TOE")
    print("=" * 50)
    print(f"AI: {type(ai_agent).__name__} ({ai_symbol})")
    print(f"You are {human_symbol}. Choose positions using numbers 0–8.\n")
    print("Grid Reference:\n 0 | 1 | 2\n-----------\n 3 | 4 | 5\n-----------\n 6 | 7 | 8\n")

    def display_board(s: GameState):
        b = [c if c is not None else " " for c in s.board]
        print(f"\n   {b[0]} | {b[1]} | {b[2]} ")
        print("  -----------")
        print(f"   {b[3]} | {b[4]} | {b[5]} ")
        print("  -----------")
        print(f"   {b[6]} | {b[7]} | {b[8]} \n")

    # Assign correct symbol to AI
    ai_agent.symbol = ai_symbol

    while not state.is_terminal():
        if state.to_move == ai_symbol:
            action = ai_agent.get_action(state, depth_limit)
            print(f"AI ({type(ai_agent).__name__}) chooses cell {action}")
        else:
            legal = state.get_legal_actions()
            while True:
                try:
                    user_input = input(f"Your move (choose from {legal}): ")
                    action = int(user_input)
                    if action in legal:
                        break
                    print("Invalid move. Cell occupied or out of range.")
                except ValueError:
                    print("Please enter a number between 0 and 8.")
        state = state.generate_successor(action)
        display_board(state)

    winner = state.winner()
    print("=" * 50)
    print("                 GAME OVER")
    print("=" * 50)
    if winner == ai_symbol:
        print("AI wins! Better luck next time.")
    elif winner == human_symbol:
        print("You win! Congratulations!")
    else:
        print("It's a draw!")
    print("=" * 50)
    display_board(state)


# ===============================================================
# MAIN EXECUTION
# ===============================================================
def main():
    parser = argparse.ArgumentParser(
        description="AI Tic-Tac-Toe: Watch algorithms or play against AI!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_game.py -p AlphaBetaAgent --opp MinimaxAgent
  python run_game.py --depth 3
  python run_game.py --human AlphaBetaAgent
        """
    )
    parser.add_argument(
        "-p", "--player",
        default="AlphaBetaAgent",
        choices=["MinimaxAgent", "AlphaBetaAgent", "ExpectimaxAgent"],
        help="Algorithm for Player X (default: AlphaBetaAgent)"
    )
    parser.add_argument(
        "--opp", "--opponent",
        default="ExpectimaxAgent",
        choices=["MinimaxAgent", "AlphaBetaAgent", "ExpectimaxAgent"],
        help="Algorithm for Player O (default: ExpectimaxAgent)"
    )
    parser.add_argument(
        "--depth", type=int, default=None,
        help="Maximum search depth (default: unlimited)"
    )
    parser.add_argument(
        "--human", type=str, default=None,
        choices=["MinimaxAgent", "AlphaBetaAgent", "ExpectimaxAgent"],
        help="Play against a chosen AI (AI plays as X or O, random start)"
    )

    args = parser.parse_args()

    agent_map = {
        "MinimaxAgent": MinimaxAgent(),
        "AlphaBetaAgent": AlphaBetaAgent(),
        "ExpectimaxAgent": ExpectimaxAgent(),
    }

    if args.human:
        ai_agent = agent_map[args.human]
        play_human_vs_ai(ai_agent, depth_limit=args.depth)
    else:
        agentX = agent_map[args.player]
        agentO = agent_map[args.opp]
        play_game(agentX, agentO, depth_limit=args.depth, verbose=True)


if __name__ == "__main__":
    main()
