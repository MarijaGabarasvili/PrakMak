def get_count_of_subsequence(sequence, subsequence):
    count = 0
    sub_len = len(subsequence)
    for i in range(len(sequence) - sub_len + 1):
        if sequence[i:i + sub_len] == subsequence:
            count += 1
    return count

def get_heuristic_score(state, max_player):
    if max_player == 1:
        game_score = state.score_player1 - state.score_player2
    else:
        game_score = state.score_player2 - state.score_player1

    pattern_3_scale = 0.1
    p001 = get_count_of_subsequence(state.sequence, "001")
    p010 = get_count_of_subsequence(state.sequence, "010")
    p011 = get_count_of_subsequence(state.sequence, "011")
    p100 = get_count_of_subsequence(state.sequence, "100")
    p101 = get_count_of_subsequence(state.sequence, "101")
    p110 = get_count_of_subsequence(state.sequence, "110")
    heuristic_score = game_score + pattern_3_scale * (p001 - p010 + p011 + p100 - p101 + p110)
    return heuristic_score