from computer_player import ComputerPlayer
from game_tree import GameTree

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
    
def test_2_minimax_vs_alpha_beta_play(length):
    if length < 9:
        depth_limit = length
    else:
        depth_limit = 9
    print(f"Generating game tree for seqeunce length {length} with depth limit {depth_limit}")
    tree = GameTree(length, depth_limit)
    print(f"Game tree generated. Sequence {tree.initial_sequence}, Playing game...")
    player1 = ComputerPlayer("minimax")
    player2 = ComputerPlayer("alpha_beta")
    control_player = ComputerPlayer("alpha_beta")
    
    _, result = control_player.get_path(tree.root, True)
    if result > 0:
        print("\t\tPlayer 1 should win.")
    elif result < 0:
        print("\t\tPlayer 2 should win.")
    else:
        print("\t\tThe game should end in a draw.")
    
    while tree.current_state.children:
        if tree.get_current_player() == 1:
            path, _ = player1.get_path(tree.current_state, True)
            print(f"\033[31m Move #{tree.current_depth + 1}, Player 1 chose {path[1]} \033[0m")
            tree.move_to_next_state_by_child(path[1])
        else:
            path, _ = player2.get_path(tree.current_state, False)
            print(f"\033[32m Move #{tree.current_depth + 1}, Player 2 chose {path[1]} \033[0m")
            tree.move_to_next_state_by_child(path[1])
            
    print("Game over. Result:")
    tree.print_tree(tree.root)
    print(f"Player 1 (minimax) looked at {player1.nodes_visited} nodes,")
    print(f"Player 2 (alpha-beta) looked at {player2.nodes_visited} nodes.")

    
    


# test_1_path_result_consistency(5, 9)
test_2_minimax_vs_alpha_beta_play(9)