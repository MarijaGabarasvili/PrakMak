# GameState and GameTree classes for a simple game tree in Mākslīgā intelekta pamati course.
# v1.0, 04.03.2025
# Janis Snikers

import random
import sys

from collections import deque

class GameState:
    sequence: str
    """Sequence of '0' and '1' representing the current state."""
    score_player1: int
    """Score of player 1."""
    score_player2: int
    """Score of player 2."""
    
    def __init__(self, sequence : str, score_player1 : int, score_player2 : int):
        self.sequence = sequence              # Now stored as a string of '0' and '1'
        self.score_player1 = score_player1
        self.score_player2 = score_player2
        self.children = []                    # List of subsequent states

    def __repr__(self):
        return (f"Seq: {self.sequence} | "
                f"Score (P1:P2): {self.score_player1}:{self.score_player2} | ")
    
    @staticmethod
    def get_size(node) -> int:
        """Estimates the size of a single node in bytes."""
        return (sys.getsizeof(node) 
                + sys.getsizeof(node.sequence) 
                + sys.getsizeof(node.children) 
                + sys.getsizeof(node.score_player1) 
                + sys.getsizeof(node.score_player2))


class GameTree:
    initial_sequence: str
    """Randomly generated initial sequence of '0' and '1' representing the starting state."""
    root: GameState
    """Pointer to the root node of the game tree."""
    current_state: GameState
    """Pointer to the current state in the game tree."""
    current_player: int
    """Current player (1 or 2)."""
    current_depth: int
    """Current move number (depth of the tree) in the game."""
    
    def __init__(self, sequence_length: int, depth_limit: int = 5):
        self.initial_sequence = GameTree._generate_random_sequence(sequence_length)
        self.root = GameState(
            self.initial_sequence, score_player1=0, score_player2=0
        )
        self.current_state = self.root
        self.depth_limit = depth_limit
        self.current_depth = 0
        self.current_player = 1
        self._build_tree(self.root)
        
    def __repr__(self):
        return (f"Move #: {self.current_depth} | "
                f"Player: {self.current_player} | "
                f"Sequence: {self.current_state.sequence} | "
                f"Score: {self.current_state.score_player1}:{self.current_state.score_player2} | ")

    def move_to_next_state_by_child(self, child_node : GameState):
        """Advances the game to the next state based on the selected child node.
        Purges all children nodes that are not needed anymore and generates the next game tree level if needed."""	
        if child_node not in self.current_state.children:
            raise ValueError("Given node is not a child of the current state.")
        self.current_state.children = [child_node]
        self.current_state = child_node
        self.current_depth += 1
        self.current_player = 1 if self.current_depth % 2 == 0 else 2
        self._build_tree(self.current_state)
    
    def move_to_next_state_by_move(self, first_digit_to_join: int):
        """
        Advances the game by merging the pair at 'first_digit_to_join'.
        """
        # We simply call the _merge_pair helper once.
        new_node = self._merge_pair(
            parent_node=self.current_state, 
            first_digit_to_join=first_digit_to_join, 
            depth=self.current_depth
        )
        
        # Replace children with only this newly chosen node
        self.current_state.children = [new_node]

        # Advance
        self.current_state = new_node
        self.current_depth += 1
        self.current_player = 1 if self.current_depth % 2 == 0 else 2

        # (Optional) expand the new node's children if within depth
        self._build_tree(self.current_state)
        
    def current_player(self):
        """Returns the current player (1 or 2)."""
        return 1 if self.current_depth % 2 == 0 else 2
    
    @staticmethod       
    def print_tree(node, prefix="", is_last=True):
        """Prints the tree structure starting from the given node. Use with caution for large trees."""
        connector = "└── " if is_last else "├── "
        print(prefix + connector + str(node))
        
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        child_count = len(node.children)
        for i, child in enumerate(node.children):
            GameTree.print_tree(child, new_prefix, i == child_count - 1)
    
    @staticmethod        
    def print_stats(node : GameState):
        """ Recalculates node count and memory usage from the current state down."""
        node_count = 0
        size_in_bytes = 0

        def traverse(node):
            nonlocal node_count, size_in_bytes
            node_count += 1
            size_in_bytes += GameState.get_size(node)
            for child in node.children:
                traverse(child)

        traverse(node)
        
        def _get_readable_size(size_in_bytes: int) -> str:
            if size_in_bytes >= 1024**3:  # 1 GB or more
                return f"{size_in_bytes // 1024**3} GB"
            elif size_in_bytes >= 1024**2:  # 1 MB or more
                return f"{size_in_bytes // 1024**2} MB"
            elif size_in_bytes >= 1024:  # 1 KB or more
                return f"{size_in_bytes // 1024} KB"
            else:
                return f"{size_in_bytes} Bytes"  # Less than 1 KB
        
        formated_node_count = f"{node_count:_}".replace("_", " ")
        print(f"{formated_node_count} nodes, {_get_readable_size(size_in_bytes)}")

    def _build_tree(self, node, depth: int = 0):
        """
        Recursively build or expand the tree down to the depth_limit (DFS).
        """
        if depth >= self.depth_limit:
            return
        if len(node.sequence) <= 1:
            return

        if not node.children:
            node.children = self._generate_children(node, depth)

        for child in node.children:
            self._build_tree(child, depth + 1)

    @staticmethod
    def _generate_random_sequence(length: int) -> str:
        """Generate a random string of '0's and '1's."""
        return "".join(random.choice(['0','1']) for _ in range(length))
              
    @staticmethod
    def _merge_pair(parent_node: GameState, first_digit_to_join: int, depth: int) -> GameState:
        """
        Helper to produce a single child node by merging the two adjacent bits
        in parent_node.sequence starting at 'first_digit_to_join'.
        """
        seq = parent_node.sequence

        # Safety check for index
        if not (0 <= first_digit_to_join < len(seq) - 1):
            raise ValueError(f"Invalid index {first_digit_to_join} for sequence {seq}")

        # Determine the pair
        pair = (seq[first_digit_to_join], seq[first_digit_to_join + 1])

        # Current player logic
        current_player = 1 if depth % 2 == 0 else 2

        # Determine new digit & score change
        if pair == ('0', '0'):
            new_digit = '1'
            score_change = +1
        elif pair == ('0', '1'):
            new_digit = '0'
            score_change = -1
        elif pair == ('1', '0'):
            new_digit = '1'
            score_change = -1
        elif pair == ('1', '1'):
            new_digit = '0'
            score_change = +1

        # Construct new sequence
        new_sequence = seq[:first_digit_to_join] + new_digit + seq[first_digit_to_join + 2:]

        # Update scores
        if current_player == 1:
            new_score_p1 = parent_node.score_player1 + score_change
            new_score_p2 = parent_node.score_player2
        else:
            new_score_p1 = parent_node.score_player1
            new_score_p2 = parent_node.score_player2 + score_change

        # Create the new child node
        return GameState(
            sequence=new_sequence,
            score_player1=new_score_p1,
            score_player2=new_score_p2
        )

    @staticmethod
    def _generate_children(parent_node: GameState, depth: int = 0):
        """
        Generate all child GameStates, but now re-use the _merge_pair helper
        so we don't duplicate logic.
        """
        children = []
        for i in range(len(parent_node.sequence) - 1):
            # Just call _merge_pair for each possible pair
            child = GameTree._merge_pair(parent_node, i, depth)
            children.append(child)
        return children

    @staticmethod
    def print_unique_states(game_tree_root : GameState):
        """
        Prints total and unique node counts at each level, based on (sequence, score1, score2).
        """
        if not game_tree_root:
            print("Tree is empty.")
            return

        queue = deque([(game_tree_root, 0)])  # (node, level)
        level_counts = {}
        unique_states = {}

        while queue:
            node, level = queue.popleft()

            if level not in level_counts:
                level_counts[level] = 0
                unique_states[level] = set()

            # Increment total count
            level_counts[level] += 1

            # Store unique states based on (sequence, P1 score, P2 score)
            state_key = (node.sequence, node.score_player1, node.score_player2)
            unique_states[level].add(state_key)

            # Add children to queue
            for child in node.children:
                queue.append((child, level + 1))

        print("\n### Node Count per Level")
        print("| Level | Total States | Unique States |")
        print("|-------|--------------|---------------|")

        for level in sorted(level_counts.keys()):
            total = f"{level_counts[level]:,}"
            unique = f"{len(unique_states[level]):,}"
            print(f"| {level:<5} | {total:<12} | {unique:<13} |")

    @staticmethod
    def print_states_at_level_sorted(root : GameState, target_depth : int):
        """
        Prints all nodes at a specific level, sorted by (sequence, P1 score, P2 score),
        formatted as a Markdown table.
        """
        if not root:
            print("Tree is empty.")
            return

        queue = deque([(root, 0)])  # (node, current_level)
        level_nodes = []

        # Collect nodes at target_level
        while queue:
            node, level = queue.popleft()
            if level == target_depth:
                level_nodes.append(node)
            if level > target_depth:
                break

            for child in node.children:
                queue.append((child, level + 1))

        if not level_nodes:
            print(f"No nodes found at level {target_depth}.")
            return

        # Sort nodes by (sequence, player 1 score, player 2 score)
        level_nodes.sort(key=lambda n: (n.sequence, n.score_player1, n.score_player2))

        # Print table
        print(f"\n### Nodes at Level {target_depth}")
        print("| Sequence        | P1 Score | P2 Score |")
        print("|----------------|----------|----------|")

        for node in level_nodes:
            # node.sequence is already a string
            sequence_str = node.sequence  
            print(f"| {sequence_str:<16} | {node.score_player1:<8} | {node.score_player2:<8} |")


