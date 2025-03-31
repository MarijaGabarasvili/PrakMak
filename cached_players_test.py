from game_tree import GameTree
import time

def get_count_of_subsequence(sequence, subsequence):
    count = 0
    sub_len = len(subsequence)
    for i in range(len(sequence) - sub_len + 1):
        if sequence[i:i + sub_len] == subsequence:
            count += 1
    return count

def get_heuristic_score(state):
    pattern_3_scale = 0.1
    p001 = get_count_of_subsequence(state.sequence, "001")
    p010 = get_count_of_subsequence(state.sequence, "010")
    p011 = get_count_of_subsequence(state.sequence, "011")
    p100 = get_count_of_subsequence(state.sequence, "100")
    p101 = get_count_of_subsequence(state.sequence, "101")
    p110 = get_count_of_subsequence(state.sequence, "110")
    
    p11 = get_count_of_subsequence(state.sequence, "11")
    p00 = get_count_of_subsequence(state.sequence, "00")
    
    if(p11+p00 ==1):
        p2 = 1
    else:
        p2 = 0
        
    state_score = state.score_player1 - state.score_player2
    
    heuristic_score = state_score + pattern_3_scale * (p001 - p010 + p011 + p100 - p101 + p110 - p2)
        
    return heuristic_score

# update the minimax function to use the cache
def minimax(state_node, is_maximizing: bool, cache={}):
    state_hash = (state_node.sequence, state_node.score_player1, state_node.score_player2)
    
    if state_hash in cache:
        return cache[state_hash]
    
    if not state_node.children:
        score = get_heuristic_score(state_node)
        cache[state_hash] = (score, [state_node])
        return score, [state_node]
    
    optimal_path = []
    
    if is_maximizing:
        best_score = -float('inf')
        for child in state_node.children:
            score, path = minimax(child, False, cache)
            if score > best_score:
                best_score = score
                optimal_path = [state_node] + path
    else:
        best_score = float('inf')
        for child in state_node.children:
            score, path = minimax(child, True, cache)
            if score < best_score:
                best_score = score
                optimal_path = [state_node] + path
    
    cache[state_hash] = (best_score, optimal_path)
    return best_score, optimal_path


def alpha_beta(state_node, is_maximizing, alpha=-float('inf'), beta=float('inf'), cache={}):
    # Create a unique hash for the current state.
    state_hash = (state_node.sequence, state_node.score_player1, state_node.score_player2)
    
    # If this state has been computed before, return the cached value.
    if state_hash in cache:
        return cache[state_hash]
    
    # Terminal node: evaluate and cache.
    if not state_node.children:
        score = get_heuristic_score(state_node)
        result = (score, [state_node])
        cache[state_hash] = result
        return result
    
    # If children haven't been generated yet.
    if state_node.children is None:
        state_node.children = GameTree.generate_children(state_node)
    
    optimal_path = []
    
    if is_maximizing:
        max_eval = -float('inf')
        for child in state_node.children:
            eval, path = alpha_beta(child, False, alpha, beta, cache)
            if eval > max_eval:
                max_eval = eval
                optimal_path = [state_node.sequence] + path
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        result = (max_eval, optimal_path)
        cache[state_hash] = result
        return result
    else:
        min_eval = float('inf')
        for child in state_node.children:
            eval, path = alpha_beta(child, True, alpha, beta, cache)
            if eval < min_eval:
                min_eval = eval
                optimal_path = [state_node.sequence] + path
            beta = min(beta, eval)
            if beta <= alpha:
                break
        result = (min_eval, optimal_path)
        cache[state_hash] = result
        return result

def heuristic_path(state_node, is_maximizing: bool):
    if not state_node.children:
        return [state_node]
    if is_maximizing:
        best_child = None
        best_score = -float('inf')
        for child in state_node.children:
            score = get_heuristic_score(child)
            if score > best_score:
                best_score = score
                best_child = child
        return [state_node] + heuristic_path(best_child, False)
    else:
        best_child = None
        best_score = float('inf')
        for child in state_node.children:
            score = get_heuristic_score(child)
            if score < best_score:
                best_score = score
                best_child = child
        return [state_node] + heuristic_path(best_child, True)

def print_path(path):
    for state in path:
        print(state)