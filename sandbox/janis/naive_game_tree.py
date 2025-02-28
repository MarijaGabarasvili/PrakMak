import random
import sys

class GameStateNode:
    def __init__(self, sequence : str, score_player1 : int, score_player2 : int, current_player : int):
        self.sequence = sequence              # A list or string of '0' and '1'
        self.score_player1 = score_player1
        self.score_player2 = score_player2
        self.current_player = current_player  # 1 or 2
        self.children = []                    # List of subsequent states

    def __repr__(self):
        # Helpful for debugging:
        return (f"Sequence: {self.sequence} | "
                f"Scores: P1={self.score_player1}, P2={self.score_player2} | "
                f"Current Player: {self.current_player}")
        
    def __del__(self):
        for child in self.children:
            del child
        self.children.clear()

class GameTree:
    def __init__(self, sequence_length : int):
        self.starting_sequence = GameTree._generate_random_sequence(sequence_length)
        self.root = GameStateNode(self.starting_sequence,
                                     score_player1=0,
                                     score_player2=0,
                                     current_player=1)
        self.stats_node_count = 0
        self.stats_size_in_bytes = 0
        self._build_tree(self.root)
    
    def __repr__(self):
        GameTree._print_tree(self.root)
        return ""

    @staticmethod
    def _generate_random_sequence(length : int):
        return [random.choice([0, 1]) for _ in range(length)]
    
    def _build_tree(self, node):
        
        self.stats_node_count += 1
        self.stats_size_in_bytes += GameTree._get_node_size(node)
        
        if len(node.sequence) == 1:
            # Terminal node: no children, game is over
            return

        # Generate children
        node.children = GameTree._generate_children(node)

        # Recursively build the tree for each child
        for child in node.children:
            self._build_tree(child)
                
    @staticmethod
    def _generate_children(parent_node : GameStateNode):
        parent_sequence = parent_node.sequence
        children = []

        for i in range(len(parent_sequence) - 1):
            pair = (parent_sequence[i], parent_sequence[i+1])

            # Determine the replacement digit and the score delta
            if pair == (0, 0):
                new_digit = 1
                score_change = +1
            elif pair == (0, 1):
                new_digit = 0
                score_change = -1
            elif pair == (1, 0):
                new_digit = 1
                score_change = -1
            elif pair == (1, 1):
                new_digit = 0
                score_change = +1

            # Build the new sequence
            new_sequence = parent_sequence[:i] + [new_digit] + parent_sequence[i+2:]

            # Update scores
            if parent_node.current_player == 1:
                new_score_p1 = parent_node.score_player1 + score_change
                new_score_p2 = parent_node.score_player2
                new_player = 2
            else:
                new_score_p1 = parent_node.score_player1
                new_score_p2 = parent_node.score_player2 + score_change
                new_player = 1

            # Create child node
            child = GameStateNode(sequence=new_sequence,
                                score_player1=new_score_p1,
                                score_player2=new_score_p2,
                                current_player=new_player)
            children.append(child)

        return children

    @staticmethod
    def _get_node_size(node):
        # Estimates the size of a single node in bytes.
        return (sys.getsizeof(node) + sys.getsizeof(node.sequence) + 
                sys.getsizeof(node.children) + sys.getsizeof(node.score_player1) + 
                sys.getsizeof(node.score_player2) + sys.getsizeof(node.current_player))
    
    @staticmethod       
    def _print_tree(node, prefix="", is_last=True):
        # Determine the appropriate tree structure symbols
        connector = "└── " if is_last else "├── "
        print(prefix + connector + str(node))
        
        # Update prefix for children
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        # Iterate through children
        child_count = len(node.children)
        for i, child in enumerate(node.children):
            GameTree._print_tree(child, new_prefix, i == child_count - 1)
    @staticmethod
    def _get_readable_size(size_in_bytes: int) -> str:
        """Converts bytes into a human-readable format (KB, MB, GB) with integer values."""
        if size_in_bytes >= 1024**3:  # 1 GB or more
            return f"{size_in_bytes // 1024**3} GB"
        elif size_in_bytes >= 1024**2:  # 1 MB or more
            return f"{size_in_bytes // 1024**2} MB"
        elif size_in_bytes >= 1024:  # 1 KB or more
            return f"{size_in_bytes // 1024} KB"
        else:
            return f"{size_in_bytes} Bytes"  # Less than 1 KB

    def print_stats(self):
        formated_node_count = f"{self.stats_node_count:_}".replace("_", " ")
        print(f"{formated_node_count} nodes, {GameTree._get_readable_size(self.stats_size_in_bytes)}")
