import random
import time

from no_duplicates_game_tree import GameTree

# ------------------------------------------------------------------------------------------------------------
# Example usage/test for GameTree. Trying to generate as big as possible full tree. 11 levels is around
# 30 sec and 2GB Ram on my machine
# ------------------------------------------------------------------------------------------------------------
def test_2_how_big_tree_can_be_generated():
    print("# Test 2: Tree size")
    depth_limit = sequence_length = 20
    print(f"\n\n\033[92m## Generating GameTree({sequence_length})\033[0m")
    start_time = time.time()
    game = GameTree(sequence_length, depth_limit)
    time_elapsed = time.time() - start_time
    print(f"generation took {time_elapsed:.6f} seconds, it`s size:")
    GameTree.print_stats(game.root)
    print("")
    GameTree.print_unique_states(game.root)
        
test_2_how_big_tree_can_be_generated()