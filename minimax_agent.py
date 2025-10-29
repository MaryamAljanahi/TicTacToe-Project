# minimax_agent.py
from agent_base import Agent
from game import GameState

class MinimaxAgent(Agent):
    def get_action(self, state: GameState, depth=None):
        _, action = self.minimax(state)
        return action

    def minimax(self, state, depth_limit=None):
        """
        Returns: (value, best_action)
        
        TODO: Implement the minimax algorithm here.
        
        The algorithm should:
        1. Check if the state is terminal and return (utility, None) if so
        2. For MAX player ('X'): find the action that maximizes the minimum value
        3. For MIN player ('O'): find the action that minimizes the maximum value
        4. Recursively call minimax on successor states
        5. Return the best value and corresponding action as a tuple
        
        Hint: Use state.is_terminal(), state.utility(), state.get_legal_actions(),
              state.generate_successor(), and state.to_move
        """
        # TODO: Remove this line and implement the minimax algorithm
        if state.is_terminal():
            return state.utility(), None

        player = state.to_move
        best_action = None

        if player == 'X':  # MAX player
            best_value = float('-inf')
            for action in state.get_legal_actions():
                successor = state.generate_successor(action)
                value, _ = self.minimax(successor)
                if value > best_value:
                    best_value = value
                    best_action = action
            return best_value, best_action

        else:  # MIN player
            best_value = float('inf')
            for action in state.get_legal_actions():
                successor = state.generate_successor(action)
                value, _ = self.minimax(successor)
                if value < best_value:
                    best_value = value
                    best_action = action
            return best_value, best_action


