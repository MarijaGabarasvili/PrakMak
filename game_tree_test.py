import random
import time

from game_tree import GameTree

# ------------------------------------------------------------------------------------------------------------
# Usage example for printing full tree structure and stats
# This is a very small tree, so it's not a problem:
# ------------------------------------------------------------------------------------------------------------
def test_1_print_full_tree():
    print("# Test 1: Full tree")
    depth_limit = sequence_length= 4
    print(f"\n\n## Generating GameTree({sequence_length}) ")
    start_time = time.time()
    game = GameTree(sequence_length, depth_limit)
    time_elapsed = time.time() - start_time
    print(f"generation took {time_elapsed:.6f} seconds, it`s size:")
    GameTree.print_stats(game.root)
    print("")
    GameTree.print_unique_states(game.root)
    GameTree.print_states_at_level_sorted(game.root, 2)
    print("```")
    GameTree.print_tree(game.root)
    print("```")
    
# ------------------------------------------------------------------------------------------------------------
# Example usage/test for GameTree. Trying to generate as big as possible full tree. 11 levels is around
# 30 sec and 2GB Ram on my machine
# ------------------------------------------------------------------------------------------------------------
def test_2_how_big_tree_can_be_generated():
    print("# Test 2: Tree size")
    depth_limit = sequence_length = 16
    print(f"\n\n\033[92m## Generating GameTree({sequence_length})\033[0m")
    start_time = time.time()
    game = GameTree(sequence_length, depth_limit)
    time_elapsed = time.time() - start_time
    print(f"generation took {time_elapsed:.6f} seconds, it`s size:")
    GameTree.print_stats(game.root)
    print("")
    GameTree.print_unique_states(game.root)

def test_3_traverse_by_positive_moves():
    print("# Test 4: Random moves by selecting moves that yield +1 score for the current player, with fallback to any random move")
    depth_limit = 7
    sequence_length = 15

    print(f"\n\n## Generating GameTree({sequence_length}) ")
    start_time = time.time()
    game = GameTree(sequence_length, depth_limit)
    time_elapsed = time.time() - start_time
    print(f"Generation took {time_elapsed:.6f} seconds")
    GameTree.print_stats(game.root)

    print("\n# Randomly traversing with positive moves until reaching a terminal state...\n")
    move_count = 0


    while game.current_state.children:
        # Color output based on the current player
        if game.get_current_player() == 1:
            print("\033[91m")
        else:
            print("\033[92m")
        print(game)
        # Filter moves that yield a +1 score for the current player
        positive_moves = []
        GameTree.print_states_at_level_sorted(game.root, game.current_depth + 1)
        for child in game.current_state.children:
            if game.get_current_player() == 1:
                if (child.score_player1 - game.current_state.score_player1) == 1:
                    positive_moves.append(child)
            else:
                if (child.score_player2 - game.current_state.score_player2) == 1:
                    positive_moves.append(child)
        
        if positive_moves:
            # Choose one of the positive moves at random.
            random_child = random.choice(positive_moves)
            print("Positive move available. Choosing one randomly.")
        else:
            # Fallback: choose any available move at random.
            random_child = random.choice(game.current_state.children)
            print("No positive move available. Falling back to any random move.")
            #GameTree.print_states_at_level_sorted(game.root, game.current_depth + 1)

        start_move = time.time()
        game.move_to_next_state_by_child(random_child)
        end_move = time.time()
        move_count += 1
        move_ms = (end_move - start_move)
        print(f"Move {move_count} took {move_ms:.12f} s")
        #print(game)
        #GameTree.print_stats(game.root)

    print("\033[0m")
    print("\nGame ended. Final tree structure from root:")
    GameTree.print_tree(game.root)

#test_1_print_full_tree()        
test_2_how_big_tree_can_be_generated()
#test_3_traverse_by_positive_moves()