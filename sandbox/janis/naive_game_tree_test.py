import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from sandbox.janis.naive_game_tree import GameTree
from sandbox.janis.naive_game_tree import print_unique_states_at_level
from sandbox.janis.naive_game_tree import print_states_at_level_sorted

import time



        

# Usage example:
sequence_length = 5
print(f"\n\n# Generating GameTree({sequence_length}) ")
start_time = time.time()
game = GameTree(sequence_length)
time_elapsed = time.time() - start_time
print(f"generation took {time_elapsed:.6f} seconds, it`s size:")
game.print_stats()
print("")
print_unique_states_at_level(game.root)
print_states_at_level_sorted(game.root, 3)
print("```")
print(game)
print("```")

sequence_length = 7
print(f"\n\n# Generating GameTree({sequence_length}) ")
start_time = time.time()
game = GameTree(sequence_length)
time_elapsed = time.time() - start_time
print(f"generation took {time_elapsed:.6f} seconds, it`s size:")
game.print_stats()
print("")
print_unique_states_at_level(game.root)

sequence_length = 9
print(f"\n\n# Generating GameTree({sequence_length}) ")
start_time = time.time()
game = GameTree(sequence_length)
time_elapsed = time.time() - start_time
print(f"generation took {time_elapsed:.6f} seconds, it`s size:")
game.print_stats()
print("")
print_unique_states_at_level(game.root)

sequence_length = 11
print(f"\n\n# Generating GameTree({sequence_length}) ")
start_time = time.time()
game = GameTree(sequence_length)
time_elapsed = time.time() - start_time
print(f"generation took {time_elapsed:.6f} seconds, it`s size:")
game.print_stats()
print("")
print_unique_states_at_level(game.root)
