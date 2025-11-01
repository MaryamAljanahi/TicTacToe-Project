# alphabeta_agent.py
from agent_base import Agent
from game import GameState
from evaluation import betterEvaluationFunction

class AlphaBetaAgent(Agent):
    def get_action(self, state: GameState, depth=None):
        """
        Returns the best move index (0-8) for Tic-Tac-Toe using Alpha-Beta pruning.
        """
        value, action = self.alphabeta(state, alpha=float('-inf'), beta=float('inf'),
                                       depth_limit=depth, current_depth=0)
        # Safety fallback (never return None)
        if action is None:
            legal = state.get_legal_actions()
            if legal:
                action = legal[0]
        return action

    def alphabeta(self, state: GameState, alpha, beta, depth_limit, current_depth):
        """
        Recursive alpha-beta search returning (value, best_action).
        
        TODO: Implement the alpha-beta pruning algorithm here.
        
        The algorithm should:
        1. Check if the state is terminal and return (utility, None) if so
        2. Check if depth limit is reached and use heuristic evaluation if so
        3. For MAX player ('X'): 
           - Find action that maximizes value
           - Update alpha and prune when alpha >= beta
        4. For MIN player ('O'):
           - Find action that minimizes value  
           - Update beta and prune when beta <= alpha
        5. Return the best value and corresponding action as a tuple
        
        Hint: Use betterEvaluationFunction(state) for non-terminal cutoff evaluation
        """
        # TODO: Remove this line and implement the alpha-beta algorithm
 # Base case: terminal state
        if state.is_terminal():
            return state.utility(), None

        # Depth limit reached — use heuristic evaluation
        if depth_limit is not None and current_depth == depth_limit:
            return betterEvaluationFunction(state), None

        legal_actions = state.get_legal_actions()
        best_action = None

        # MAX player (X)
        if state.player == 'X':
            value = float('-inf')
            for action in legal_actions:
                successor = state.generate_successor(action)
                child_value, _ = self.alphabeta(successor, alpha, beta, depth_limit, current_depth + 1)

                if child_value > value:
                    value = child_value
                    best_action = action

                alpha = max(alpha, value)
                if alpha >= beta:  # prune
                    break
            return value, best_action

        # MIN player (O)
        else:
            value = float('inf')
            for action in legal_actions:
                successor = state.generate_successor(action)
                child_value, _ = self.alphabeta(successor, alpha, beta, depth_limit, current_depth + 1)

                if child_value < value:
                    value = child_value
                    best_action = action

                beta = min(beta, value)
                if beta <= alpha:  # prune
                    break
            return value, best_action
        
