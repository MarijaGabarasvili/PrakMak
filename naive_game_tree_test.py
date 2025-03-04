import random
import time

from naive_game_tree import GameTree

# ------------------------------------------------------------------------------------------------------------
# Usage example for printing full tree structure and stats
# This is a very small tree, so it's not a problem:
# ------------------------------------------------------------------------------------------------------------
def test_1_print_full_tree():
    print("# Test 1: Full tree")
    depth_limit = sequence_length= 5
    print(f"\n\n## Generating GameTree({sequence_length}) ")
    start_time = time.time()
    game = GameTree(sequence_length, depth_limit)
    time_elapsed = time.time() - start_time
    print(f"generation took {time_elapsed:.6f} seconds, it`s size:")
    GameTree.print_stats(game.root)
    print("")
    GameTree.print_unique_states(game.root)
    GameTree.print_states_at_level_sorted(game.root, 3)
    print("```")
    GameTree.print_tree(game.root)
    print("```")

# ------------------------------------------------------------------------------------------------------------
# Example usage/test for GameTree. Trying to generate as big as possible full tree. 11 levels is around
# 30 sec and 2GB Ram on my machine
# ------------------------------------------------------------------------------------------------------------
def test_2_how_big_tree_can_be_generated():
    print("# Test 2: Tree size")
    for i in range(5, 12, 2):
        depth_limit = sequence_length = i
        print(f"\n\n\033[92m## Generating GameTree({sequence_length})\033[0m")
        start_time = time.time()
        game = GameTree(sequence_length, depth_limit)
        time_elapsed = time.time() - start_time
        print(f"generation took {time_elapsed:.6f} seconds, it`s size:")
        GameTree.print_stats(game.root)
        print("")
        GameTree.print_unique_states(game.root)
    
# ------------------------------------------------------------------------------------------------------------
# Example usage/test for GameTree. Limited depth generations and random moves by selecting random child pointer
# until reaching a terminal state. A lot of time is spent on calculating tree size, so it's not a good idea to
# use this for large trees.
# ------------------------------------------------------------------------------------------------------------
def test_3_traverse_by_random_nodes():
    print("# Test 3: Random moves by selecting random child pointer")
    depth_limit = 5
    sequence_length = 15

    print(f"\n\n## Generating GameTree({sequence_length}) ")
    start_time = time.time()
    game = GameTree(sequence_length, depth_limit)
    time_elapsed = time.time() - start_time
    print(f"Generation took {time_elapsed:.6f} seconds")
    print("\033[92m")
    print(game)
    GameTree.print_stats(game.root)
    print("\033[0m")

    print("\n# Randomly traversing until reaching a terminal state...\n")
    move_count = 0

    while game.current_state.children:
        
        if game.current_player == 1:
            print("\033[91m")
        else:
            print("\033[92m")

        random_child = random.choice(game.current_state.children)

        start_move = time.time()
        game.move_to_next_state_by_child(random_child)
        end_move = time.time()
        move_count += 1
        move_ms = (end_move - start_move)
        print(f"Move {move_count} took {move_ms:.12f} s")
        print(game)
        GameTree.print_stats(game.root)

    print("\033[0m")
    print("\nGame ended. Final tree structure from root:")
    GameTree.print_tree(game.root)


# ------------------------------------------------------------------------------------------------------------
# Example usage/test for GameTree. Limited depth generations and random moves by picking first number of the
# two to merge, until reaching a terminal state. A lot of time is spent on calculating tree size, so it's not
# a good idea to use this for large trees.
# ------------------------------------------------------------------------------------------------------------
def test_4_traverse_by_random_merges():
    print("# Test 4: Random moves by picking first number of the two to merge")
    depth_limit = 5
    sequence_length = 15

    print(f"\n\n## Generating GameTree({sequence_length}) ")
    start_time = time.time()
    game = GameTree(sequence_length, depth_limit)
    time_elapsed = time.time() - start_time
    print(f"Generation took {time_elapsed:.6f} seconds")
    print("\033[92m")
    print(game)
    GameTree.print_stats(game.root)
    print("\033[0m")
    
    print("\n# Randomly traversing until reaching a terminal state...\n")
    move_count = 0

    while game.current_state.children:
        if game.current_player == 1:
            print("\033[91m")
        else:
            print("\033[92m")

        seq_length = len(game.current_state.sequence)
        if seq_length <= 1:
            break
        
        random_index = random.randrange(seq_length - 1)
        
        start_move = time.time()
        game.move_to_next_state_by_move(random_index)
        end_move = time.time()

        move_count += 1
        move_ms = end_move - start_move
        print(f"Picked {random_index} and {random_index + 1}, move {move_count} took {move_ms:.12f} s, next move:")
        print(game)
        GameTree.print_stats(game.root)

    print("\033[0m")
    print("\nGame ended. Final tree structure from root:")
    GameTree.print_tree(game.root)

# test_1_print_full_tree()    
# test_2_how_big_tree_can_be_generated()
# test_3_traverse_by_random_nodes()
test_4_traverse_by_random_merges()