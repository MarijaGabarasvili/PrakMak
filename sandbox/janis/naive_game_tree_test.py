import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from sandbox.janis.naive_game_tree import GameTree

import time

# Usage example:
sequence_length = 5
start_time = time.time()
game5 = GameTree(sequence_length)
time_elapsed = time.time() - start_time
print(f"\nGameTree({sequence_length}) generation took {time_elapsed:.6f} seconds, it`s size:")
game5.print_stats()
print("")
print(game5)

sequence_length = 7
start_time = time.time()
game7 = GameTree(sequence_length)
time_elapsed = time.time() - start_time
print(f"GameTree({sequence_length}) generation took {time_elapsed:.2f} seconds, it`s size:")
game7.print_stats()
print("")

sequence_length = 9
start_time = time.time()
game9 = GameTree(sequence_length)
time_elapsed = time.time() - start_time
print(f"GameTree({sequence_length}) generation took {time_elapsed:.2f} seconds, it`s size:")
game9.print_stats()
print("")

sequence_length = 11
start_time = time.time()
game11 = GameTree(sequence_length)
time_elapsed = time.time() - start_time
print(f"GameTree({sequence_length}) generation took {time_elapsed:.2f} seconds, it`s size:")
game11.print_stats()
print("")
