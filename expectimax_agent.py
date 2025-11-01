# expectimax_agent.py
from agent_base import Agent
from game import GameState
from evaluation import betterEvaluationFunction

class ExpectimaxAgent(Agent):
    def get_action(self, state: GameState, depth=None):
        """
        Returns the best move index (0-8) using Expectimax search.
        Handles stochastic (non-optimal) opponent moves.
        """
        value, action = self.expectimax(state, depth_limit=depth, current_depth=0)
        # Safety fallback in case no action is found
        if action is None:
            legal = state.get_legal_actions()
            if legal:
                action = legal[0]
        return action

    def expectimax(self, state: GameState, depth_limit, current_depth):
        """
        Recursive Expectimax returning (value, best_action)
        
        TODO: Implement the expectimax algorithm here.
        
        The algorithm should:
        1. Check if the state is terminal and return (utility, None) if so
        2. Check if depth limit is reached and use heuristic evaluation if so
        3. For MAX node ('X'): find the action that maximizes expected value
        4. For CHANCE node ('O'): calculate expected value by averaging over all possible actions
           (assumes opponent plays randomly with uniform probability)
        5. Return the value and best action as a tuple
        
        Hint: For chance nodes, you'll need to average the values of all successor states.
              Use betterEvaluationFunction(state) for non-terminal cutoff evaluation.
        """
        # Terminal check
        if state.is_terminal():
            return state.utility(), None

        # Cutoff check
        if depth_limit is not None and current_depth >= depth_limit:
            return betterEvaluationFunction(state), None

        # TODO: Implement the expectimax algorithm logic here
                legal_actions = state.get_legal_actions()

        player = state.to_move
        #if max:
        if player == 'X':
            best_val=-float('inf')
            best_action = None
            for action in legal_actions:
                successor = state.generate_successor(action)
                value, _ = self.expectimax(successor, depth_limit, current_depth+1)
                if value > best_val:
                    best_val = value
                    best_action = action
            return best_val, best_action
        #if chance
        else:
            total_value = 0
            for action in legal_actions:
                successor = state.generate_successor(action)
                value, _ = self.expectimax(successor,depth_limit, current_depth+1)
                total_value += value

            expected_value = total_value / len(legal_actions) #avg
            return expected_value, None
        # Remove this line and implement the algorithm
        # raise NotImplementedError("Expectimax algorithm not implemented yet")
