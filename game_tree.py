import random
import sys
import math

from collections import deque

str_blue = "\033[34m"
str_red = "\033[31m"
str_green = "\033[32m"
str_yellow = "\033[33m"
str_reset = "\033[0m"

class GameState:
    sequence: str
    """Sequence of '0' and '1' representing the current state."""
    score_player1: int
    """Score of player 1."""
    score_player2: int
    """Score of player 2."""
    children: list
    """List of subsequent states."""
    
    def __init__(self, sequence : str, score_player1 : int, score_player2 : int):
        self.sequence = sequence
        self.score_player1 = score_player1
        self.score_player2 = score_player2
        self.children = []

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
    current_depth: int
    """Current move number (depth of the tree) in the game."""
    
    def __init__(self, sequence, dynamic_depth: bool = True, depth_limit: int = 5):
        if isinstance(sequence, int) and sequence > 0:
            self.initial_sequence = GameTree._generate_random_sequence(sequence)
        elif isinstance(sequence, str) and all(c in '01' for c in sequence):
            self.initial_sequence = sequence
        else:
            raise ValueError("Invalid sequence provided. Must be a integer length or string of '0's and '1's.")
        self.root = GameState(
            self.initial_sequence, score_player1=0, score_player2=0
        )
        self.dynamic_depth = dynamic_depth
        self.current_state = self.root
        self.depth_limit = depth_limit
        self.current_depth = 0
        self._build_tree()
        
    def __repr__(self):
        return (f"Move #: {self.current_depth} | "
                f"Player: {self.get_current_player()} | "
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
        self._build_tree()
    
    def move_to_next_state_by_move(self, first_digit_to_join: int):
        """
        Advances the game by merging the pair at 'first_digit_to_join'.
        """
        new_state = self._create_child(
            parent_node=self.current_state, 
            first_digit_to_join=first_digit_to_join, 
            depth=self.current_depth
        )
        
        for child in self.current_state.children:
            if child.sequence == new_state.sequence:
                new_state = child
                break
        
        self.move_to_next_state_by_child(new_state)
        
    def get_current_player(self, at_depth=None) -> int:
        """Returns the current player (1 or 2)."""
        if at_depth is None:
            at_depth = self.current_depth
        return 1 if at_depth % 2 == 0 else 2
    
    def _update_depth_limit(self):
        depth_limit = math.floor(-0.375 * len(self.current_state.sequence)+12.375)
        if depth_limit < 3:
            return 3
        elif depth_limit > len(self.current_state.sequence):
            return len(self.current_state.sequence)
        return depth_limit
        
            
    
    
    def _build_tree(self):
        """
        Build the game tree up to self.depth_limit layers, unifying duplicate children
        across each layer (i.e., if two parents at the same layer generate an identical
        (sequence, score_p1, score_p2) child, they will reference the same child node).
        """
        if self.dynamic_depth:
            self.depth_limit = self._update_depth_limit()
        print(f"Building tree, depth limit {self.depth_limit}...")
        current_layer = [self.current_state]
        parent_layer_depth = self.current_depth
            
        while parent_layer_depth < (self.current_depth + self.depth_limit):
            parents_and_children = []

            # 1) Generate children for each node in the current layer (if needed)
            for node in current_layer:
                # Only generate if node has length > 1 and hasn't generated children yet
                if len(node.sequence) > 1 and not node.children:
                    node.children = self._populate_children(node, parent_layer_depth)

                # Keep track of (parent, [children]) to unify references
                parents_and_children.append((node, node.children))

            # 2) Unify duplicate children across the entire layer
            layer_dict = {}  # maps (sequence, score_p1, score_p2) -> canonical GameState
            for parent, child_list in parents_and_children:
                for i, child in enumerate(child_list):
                    key = (child.sequence, child.score_player1, child.score_player2)
                    if key not in layer_dict:
                        layer_dict[key] = child  # first time we see this child
                    else:
                        # Duplicate => replace the parent's child reference
                        parent.children[i] = layer_dict[key]

            # 3) Prepare the next layer
            # All unique children are taken from layer_dict
            next_layer = list(layer_dict.values())
            if not next_layer:
                break

            current_layer = next_layer
            parent_layer_depth += 1
            
        self._last_build_layer = current_layer
        self._last_build_depth = parent_layer_depth
              
    def _create_child(self, parent_node: GameState, first_digit_to_join: int, depth: int) -> GameState:
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

        #make it a separate function so i can use it in the main file
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
        if self.get_current_player(depth) == 1:
            new_score_p1 = parent_node.score_player1 + score_change
            new_score_p2 = parent_node.score_player2
        else:
            new_score_p1 = parent_node.score_player1
            new_score_p2 = parent_node.score_player2 + score_change
        
        if abs(score_change) > 1:
            raise ValueError(f"Invalid score change: {score_change}, parent state: {parent_node}")
        
        # Create the new child node
        return GameState(
            sequence=new_sequence,
            score_player1=new_score_p1,
            score_player2=new_score_p2
        )

    def _populate_children(self, parent_node: GameState, depth: int = 0):
        """
        Generate all child GameStates, ensuring no duplicates are stored
        if (sequence, score_player1, score_player2) already exists.
        """
        children = []
        seen = set()
        for i in range(len(parent_node.sequence) - 1):
            child = self._create_child(parent_node, i, depth)
            child_key = (child.sequence, child.score_player1, child.score_player2)
            if child_key not in seen:
                seen.add(child_key)
                children.append(child)
        return children

    @staticmethod
    def _generate_random_sequence(length: int) -> str:
        """Generate a random string of '0's and '1's."""
        return "".join(random.choice(['0','1']) for _ in range(length))
    
    @staticmethod       
    def print_tree(node, prefix="", is_last=True, level=0):
        """Prints the tree structure starting from the given node. Use with caution for large trees."""
        connector = "└── " if is_last else "├── "
        color_code = 31 if level % 2 == 0 else 32
        text_with_color = f"\033[{color_code}m{node}\033[0m"
        print(prefix + connector + text_with_color)
        
        new_prefix = prefix + ("        " if is_last else "│       ")
        
        child_count = len(node.children)
        for i, child in enumerate(node.children):
            GameTree.print_tree(child, new_prefix, i == child_count - 1, level=level + 1)
    
    @staticmethod
    def print_stats(node: GameState):
        """
        Recalculates node count and memory usage from the current state down,
        without counting duplicates.
        """
        visited = set()
        node_count = 0
        size_in_bytes = 0

        def traverse(n: GameState):
            nonlocal node_count, size_in_bytes
            if id(n) in visited:
                return
            visited.add(id(n))

            node_count += 1
            size_in_bytes += GameState.get_size(n)
            for child in n.children:
                traverse(child)

        traverse(node)
        
        def _get_readable_size(size_in_bytes: int) -> str:
            if size_in_bytes >= 1024**3:
                return f"{size_in_bytes // 1024**3} GB"
            elif size_in_bytes >= 1024**2:
                return f"{size_in_bytes // 1024**2} MB"
            elif size_in_bytes >= 1024:
                return f"{size_in_bytes // 1024} KB"
            else:
                return f"{size_in_bytes} Bytes"  # Less than 1 KB

        formated_node_count = f"{node_count:_}".replace("_", " ")
        print(f"{formated_node_count} nodes, {_get_readable_size(size_in_bytes)}")
    
    @staticmethod
    def print_unique_states(game_tree_root: GameState):
        """
        Prints total and unique node counts at each level.
        Total states is the sum of frequencies (i.e. count of duplicate references),
        while unique states is the number of distinct nodes (by identity).
        """
        if not game_tree_root:
            print("Tree is empty.")
            return

        level_dict = {}
        level_dict[0] = { id(game_tree_root): (game_tree_root, 1) }
        current_level = 0

        # Build level-by-level counts until no children are found
        while True:
            next_level = {}
            # Iterate over all nodes at the current level
            for node_id, (node, freq) in level_dict[current_level].items():
                # Expand children (each node is expanded only once)
                for child in node.children:
                    child_id = id(child)
                    # Increase frequency if already seen at next level
                    if child_id in next_level:
                        existing_node, existing_freq = next_level[child_id]
                        next_level[child_id] = (existing_node, existing_freq + freq)
                    else:
                        next_level[child_id] = (child, freq)
            if not next_level:
                break
            level_dict[current_level + 1] = next_level
            current_level += 1

        # Print the results level by level
        print("\n### Node Count per Level")
        print("| Level | Total States | Unique States |")
        print("|-------|-------------:|--------------:|")
        for lvl in sorted(level_dict.keys()):
            total_states = sum(freq for (_, freq) in level_dict[lvl].values())
            unique_states = len(level_dict[lvl])
            print(f"| {lvl:<5} | {total_states:<12,} | {unique_states:<13,} |")


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

        print(f"\n### Nodes at Level {target_depth}")
        print("| Sequence        | P1 Score | P2 Score |")
        print("|----------------|----------|----------|")

        for node in level_nodes:
            sequence_str = node.sequence  
            print(f"| {sequence_str:<16} | {node.score_player1:<8} | {node.score_player2:<8} |")
