from game_tree import GameTree
import time

class ComputerPlayer:
    def __init__(self, algorithm: str = "minimax"):
        """
        Initialize the computer player with the chosen algorithm.
        
        Supported algorithms:
            - "minimax": Uses the minimax algorithm.
            - "alpha_beta": Uses minimax with alpha-beta pruning.
            - "heuristic": Uses a greedy heuristic path selection.
        
        :param algorithm: A string indicating the algorithm to use.
        :raises ValueError: If the provided algorithm is not supported.
        """
        valid_algorithms = {"minimax", "alpha_beta", "heuristic"}
        if algorithm not in valid_algorithms:
            raise ValueError("Unsupported algorithm. Choose minimax, alpha_beta, or heuristic.")
        self.algorithm = algorithm
        self.nodes_visited = 0  # Counter for visited nodes
        optimal_path = None

    def reset_counter(self):
        """Reset the nodes visited counter to zero."""
        self.nodes_visited = 0

    def get_path(self, state_node, is_maximizing: bool = True):
        """
        Compute the path for the current state using the chosen algorithm.
        This method also counts the visited nodes during the algorithm's execution.
        It returns both the path and the final score.
        
        :param state_node: The current game state node.
        :param is_maximizing: Flag to indicate whether the current move is maximizing.
        :return: A tuple (path, score) where path is a list of states and score is the heuristic score.
        """
        if self.algorithm == "minimax":
            score, self.optimal_path = self._minimax2(state_node, is_maximizing)
            return self.optimal_path, score
        elif self.algorithm == "alpha_beta":
            score, self.optimal_path = self._alpha_beta(state_node, is_maximizing)
            return self.optimal_path, score
        elif self.algorithm == "heuristic":
            score, self.optimal_path = self._heuristic_path(state_node, is_maximizing)
            return self.optimal_path, score
        
    def print_path(self):
        """Print the path of states."""
        for state in self.optimal_path:
            print(state)
        
    def _get_count_of_subsequence(self, sequence, subsequence):
        count = 0
        sub_len = len(subsequence)
        for i in range(len(sequence) - sub_len + 1):
            if sequence[i:i + sub_len] == subsequence:
                count += 1
        return count

    def _get_heuristic_score(self, state):
        pattern_3_scale = 0.001
        p001 = self._get_count_of_subsequence(state.sequence, "001")
        p010 = self._get_count_of_subsequence(state.sequence, "010")
        p011 = self._get_count_of_subsequence(state.sequence, "011")
        p100 = self._get_count_of_subsequence(state.sequence, "100")
        p101 = self._get_count_of_subsequence(state.sequence, "101")
        p110 = self._get_count_of_subsequence(state.sequence, "110")
        
        p11 = self._get_count_of_subsequence(state.sequence, "11")
        p00 = self._get_count_of_subsequence(state.sequence, "00")
        
        p2 = 1 if (p11 + p00) == 1 else 0
        
        state_score = state.score_player1 - state.score_player2
        
        heuristic_score = state_score + pattern_3_scale * (p001 - p010 + p011 + p100 - p101 + p110 - p2)
        return heuristic_score

    def _minimax(self, state_node, is_maximizing: bool):
        # Count this node visit.
        self.nodes_visited += 1

        if not state_node.children:
            score = self._get_heuristic_score(state_node)
            return score, [state_node]

        optimal_path = []
        if is_maximizing:
            best_score = -float('inf')
            for child in state_node.children:
                score, path = self._minimax(child, False)
                if score > best_score:
                    best_score = score
                    optimal_path = [state_node] + path
            return best_score, optimal_path
        else:
            best_score = float('inf')
            for child in state_node.children:
                score, path = self._minimax(child, True)
                if score < best_score:
                    best_score = score
                    optimal_path = [state_node] + path
            return best_score, optimal_path
    
    # update the minimax function to use the cache
    def _minimax2(self, state_node, is_maximizing: bool, cache={}):
        state_hash = (state_node.sequence, state_node.score_player1, state_node.score_player2)
        
        if state_hash in cache:
            return cache[state_hash]
        
        self.nodes_visited += 1
        
        if not state_node.children:
            score = self._get_heuristic_score(state_node)
            cache[state_hash] = (score, [state_node])
            return score, [state_node]
        
        optimal_path = []
        
        if is_maximizing:
            best_score = -float('inf')
            for child in state_node.children:
                score, path = self._minimax2(child, False, cache)
                if score > best_score:
                    best_score = score
                    optimal_path = [state_node] + path
        else:
            best_score = float('inf')
            for child in state_node.children:
                score, path = self._minimax2(child, True, cache)
                if score < best_score:
                    best_score = score
                    optimal_path = [state_node] + path
        
        cache[state_hash] = (best_score, optimal_path)
        return best_score, optimal_path

    def _alpha_beta(self, state_node, is_maximizing, alpha=-float('inf'), beta=float('inf')):
        # Count this node visit.
        self.nodes_visited += 1

        if not state_node.children:
            score = self._get_heuristic_score(state_node)
            return score, [state_node]

        # Generate children if not already set.
        if state_node.children is None:
            state_node.children = GameTree.generate_children(state_node)

        optimal_path = []
        if is_maximizing:
            max_eval = -float('inf')
            for child in state_node.children:
                eval, path = self._alpha_beta(child, False, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    optimal_path = [state_node] + path
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, optimal_path
        else:
            min_eval = float('inf')
            for child in state_node.children:
                eval, path = self._alpha_beta(child, True, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    optimal_path = [state_node] + path
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, optimal_path

    def _heuristic_path(self, state_node, is_maximizing: bool):
        """
        Greedy recursive approach: at each node, choose the child with the best immediate heuristic score.
        Returns a tuple (score, path), where score is the heuristic score at the terminal node.
        """
        # Count this node visit.
        self.nodes_visited += 1

        if not state_node.children:
            score = self._get_heuristic_score(state_node)
            return score, [state_node]

        if is_maximizing:
            best_child = None
            best_score = -float('inf')
            for child in state_node.children:
                child_score = self._get_heuristic_score(child)
                if child_score > best_score:
                    best_score = child_score
                    best_child = child
            # Recurse with the chosen child (flip the maximizing flag)
            score, path = self._heuristic_path(best_child, False)
            return score, [state_node] + path
        else:
            best_child = None
            best_score = float('inf')
            for child in state_node.children:
                child_score = self._get_heuristic_score(child)
                if child_score < best_score:
                    best_score = child_score
                    best_child = child
            score, path = self._heuristic_path(best_child, True)
            return score, [state_node] + path
