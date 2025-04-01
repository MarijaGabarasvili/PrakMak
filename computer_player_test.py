from computer_player import ComputerPlayer
from game_tree import GameTree

str_blue = "\033[34m"
str_red = "\033[31m"
str_green = "\033[32m"
str_yellow = "\033[33m"
str_reset = "\033[0m"

def test_1_path_result_consistency(sequence_length_start, sequence_length_end):
    def test_seq(sequence):
        if isinstance(sequence, int):
            depth = sequence
        elif isinstance(sequence, str):
            depth = len(sequence)
        game = GameTree(sequence, depth)
        seq_string = game.root.sequence
        player1 = ComputerPlayer("minimax")
        player2 = ComputerPlayer("alpha_beta")
        player3 = ComputerPlayer("heuristic")
        path1, score1 = player1.get_path(game.root, True)
        path2, score2 = player2.get_path(game.root, True)
        path3, score3 = player3.get_path(game.root, True)
        
        if score1 == score2 and score2 == score3:
            print(f"\033[92m Path result consistency test, sequence:{seq_string} - Passed (Nodes visited: minimax {player1.nodes_visited}, alpha-beta {player2.nodes_visited}, pure heuristics {player3.nodes_visited}) \033[0m")
        else:
            print(f"\033[91m Path result consistency test, sequence:{seq_string} - Failed (Minimax:{score1} != AlphaBeta:{score2} != Heuristics:{score3}) \033[0m")
            print(f"Minimax path:")
            player1.print_path()
            print(f"AlphaBeta path:")
            player2.print_path()
            print(f"Heuristics path:")
            player3.print_path()
        
    def alternate_string(start, n):
        result = ""
        curr = start
        for _ in range(n):
            result += curr
            curr = '1' if curr == '0' else '0'
        return result
    
    print("-------------------------------------------------------------------------------------------------------------------------------------------------")
    print("Path finding consistency test for sequence length from", sequence_length_start, "to", sequence_length_end)
    for n in range(sequence_length_start, sequence_length_end + 1):
        print(">>>>>>>>", n)

        test_seq("0" * n) # 0000...
        test_seq(alternate_string("0", n)) # 0101...
        test_seq(alternate_string("1", n)) # 1010...
        test_seq("1" * n) # 1111...
        for _ in range(4): # 4 random sequences
            test_seq(n)
    
def test_2_minimax_vs_alpha_beta_play(sequence, depth_limit):

    print(f"Generating game tree.")
    tree = GameTree(sequence, depth_limit)
    print(f"Game tree generated. Sequence {tree.initial_sequence}, depth limit:{depth_limit}, Playing game...")
    player1 = ComputerPlayer("minimax")
    player2 = ComputerPlayer("alpha_beta")
    player3 = ComputerPlayer("heuristic")
    # control_player = ComputerPlayer("alpha_beta")
    
    # _, result = control_player.get_path(tree.root, True)
    # if result > 0:
    #     print("\t\tPlayer 1 should win.")
    # elif result < 0:
    #     print("\t\tPlayer 2 should win.")
    # else:
    #     print("\t\tThe game should end in a draw.")
    
    while tree.current_state.children:
        
        if tree.get_current_player() == 1:
            print(f"{str_red}")
            print(f"Move #{tree.current_depth} - {tree.current_state}, choice by Player 1:")
            
            path1, result1 = player1.get_path(tree.current_state, True)
            print(f"\t{path1[1]} > end score > {result1}")
            
            path2, result2 = player2.get_path(tree.current_state, True)
            print(f"\t{path2[1]} > end score > {result2}")
            
            path3, result3 = player3.get_path(tree.current_state, True)
            print(f"\t{path3[1]} > end score > {result3}")
            print(f"{str_reset}")
            tree.move_to_next_state_by_child(path3[1])
        else:
            # for child in tree.current_state.children:
            #     print(f"{child}, score {player2._get_heuristic_score(child)}")
            
            
            
            print(f"{str_green}")
            print(f"Move #{tree.current_depth} - {tree.current_state}, choice by Player 2:")
            
            path1, result1 = player1.get_path(tree.current_state, False)
            print(f"\t{path1[1]} > end score > {result1}")
            
            path2, result2 = player2.get_path(tree.current_state, False)
            print(f"\t{path2[1]} > end score > {result2}")
            
            path3, result3 = player3.get_path(tree.current_state, False)
            print(f"\t{path3[1]} > end score > {result3}")
            
            print(f"{str_reset}")
            
            tree.move_to_next_state_by_child(path3[1])
    
    print(f"{str_blue}Game over. ", end="")
    
    result = tree.current_state.score_player1 - tree.current_state.score_player2
    if result > 0:
        print(f"{str_red}Player 1 won by {result} points{str_reset}")
    elif result < 0:
        print(f"{str_green}Player 2 won by {abs(result)} points{str_reset}")
    else:
        print(f"{str_yellow}Draw{str_reset}")   
    
    tree.print_tree(tree.root)
    
    
    
    print(f"Player 1 (minimax) looked at {player1.nodes_visited} nodes,")
    print(f"Player 2 (alpha-beta) looked at {player2.nodes_visited} nodes.")

    
    


# test_1_path_result_consistency(5, 9)
test_2_minimax_vs_alpha_beta_play("000000101111010", 15)

# └── Seq: 010011110 | Score (P1:P2): 0:0 |
#         └── Seq: 00011110 | Score (P1:P2): -1:0 |
#                 └── Seq: 1011110 | Score (P1:P2): -1:1 |
#                         └── Seq: 100110 | Score (P1:P2): 0:1 |
#                                 └── Seq: 10110 | Score (P1:P2): 0:0 |
#                                         └── Seq: 1010 | Score (P1:P2): -1:0 |
#                                                 └── Seq: 110 | Score (P1:P2): -1:-1 |
#                                                         └── Seq: 00 | Score (P1:P2): 0:-1 |
#                                                                 └── Seq: 1 | Score (P1:P2): 0:0 |