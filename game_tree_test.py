# This file is for testing/examples of game_tree.py
import random
import time

from game_tree import GameTree
from heuristics import get_heuristic_score

def minimax(state, is_maximizing: bool, depth=0):
    # needs to be updated to check if it`s last node in the tree and return heuristics`
    if len(state.sequence) == 1:
        score = state.score_player1 - state.score_player2
        return score, [state]

    best_path = []

    if is_maximizing:
        best_score = -float('inf')
        for child in state.children:
            score, path = minimax(child, False, depth + 1)
            if score > best_score:
                best_score = score
                best_path = [state] + path
        # if depth == 0:
        #     print(f"P1 MINIMAX Final Best Path: {' -> '.join(best_path)} | Score: {best_score}")
        return best_score, best_path
    else:
        best_score = float('inf')
        for child in state.children:
            score, path = minimax(child, True, depth + 1)
            if score < best_score:
                best_score = score
                best_path = [state] + path
        # if depth == 0:
        #     print(f"P2 MINIMAX Final Best Path: {' -> '.join(best_path)} | Score: {best_score}")
        return best_score, best_path
    
def heuristic_play(state, is_maximizing: bool, depth=0):
    if len(state.sequence) == 1:
        return [state]  # Base case: end state, return single-item path

    best_child = None
    best_score = -float('inf')
    if is_maximizing:
        
        
        for child in state.children:
            score = get_heuristic_score(child, 1)
            if score > best_score:
                best_score = score
                best_child = child
        best_path = heuristic_play(best_child, False, depth + 1)
    else:        
        for child in state.children:
            score = get_heuristic_score(child, 2)
            if score > best_score:
                best_score = score
                best_child = child
        best_path = heuristic_play(best_child, True, depth + 1)

    # Recursively follow the best child
    
    
    # Add current state to the beginning of the path
    return [state] + best_path
# ------------------------------------------------------------------------------------------------------------
# Usage example for printing full tree structure and stats
# This is a very small tree, so it's not a problem:
# ------------------------------------------------------------------------------------------------------------
def test_1_print_full_tree(sequence):
    print("# Test 1: Full tree")
    print(f"\n\n## Generating GameTree({sequence}) ")
    start_time = time.time()
    game = GameTree(sequence, len(sequence))
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



def print_path(path):
    for state in path:
        print(state)



def test_4_heuristics(sequence):
    if isinstance(sequence, int):
        depth = sequence
    elif isinstance(sequence, str):
        depth = len(sequence)
    game = GameTree(sequence, depth)
    seq_string = game.root.sequence
    score1, path1 = minimax(game.root, True)   
    path2 = heuristic_play(game.root, True)
    score2 = path2[-1].score_player1 - path2[-1].score_player2
    if score1 == score2:
        print(f"\033[92m Heuristic test, sequence:{seq_string} - Passed \033[0m")
    else:
        print(f"\033[91m Heuristic test, sequence:{seq_string} - Failed (Minimax:{score1} != Heuristics:{score2}) \033[0m")
        print(f"Minimax path:")
        print_path(path1)
        print(f"Heuristics path:")
        print_path(path2)
    
    
# test_1_print_full_tree("1010101")        
# test_2_how_big_tree_can_be_generated()
# test_3_traverse_by_positive_moves()
print("------------------------------------------------------------------------------------------------------------")
print(">>>>>>>> 5")
test_4_heuristics("00000")
test_4_heuristics("01010")
test_4_heuristics("10101")
test_4_heuristics("11111")
test_4_heuristics(5)
print(">>>>>>>> 6")
test_4_heuristics("000000")
test_4_heuristics("010101")
test_4_heuristics("101010")
test_4_heuristics("111111")
test_4_heuristics(6)
print(">>>>>>>> 7")
test_4_heuristics("0000000")
test_4_heuristics("0101010")
test_4_heuristics("1010101")
test_4_heuristics("1111111")
test_4_heuristics(7)
print(">>>>>>>> 8")
test_4_heuristics("00000000")
test_4_heuristics("01010101")
test_4_heuristics("10101010")
test_4_heuristics("11111111")
test_4_heuristics(8)
print(">>>>>>>> 9")
test_4_heuristics("000000000")
test_4_heuristics("010101010")
test_4_heuristics("101010101")
test_4_heuristics("111111111")
test_4_heuristics(9)
print(">>>>>>>> 10")
test_4_heuristics("0000000000")
test_4_heuristics("0101010101")
test_4_heuristics("1010101010")
test_4_heuristics("1111111111")
test_4_heuristics(10)
print(">>>>>>>> 11")
test_4_heuristics("00000000000")
test_4_heuristics("01010101010")
test_4_heuristics("10101010101")
test_4_heuristics("11111111111")
test_4_heuristics(11)

