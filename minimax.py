from no_duplicates_game import GameTree
import time

def minimax(node, is_maximizing: bool, depth=0):
    indent = "  " * depth

    if len(node.sequence) == 1:
        score = node.score_player1 - node.score_player2
        return score, [node.sequence]

    best_path = []

    if is_maximizing:
        best_score = -float('inf')
        for child in node.children:
            score, path = minimax(child, False, depth + 1)
            if score > best_score:
                best_score = score
                best_path = [node.sequence] + path
        if depth == 0:
            print(f"P1 MINIMAX Final Best Path: {' -> '.join(best_path)} | Score: {best_score}")
        return best_score, best_path
    else:
        best_score = float('inf')
        for child in node.children:
            score, path = minimax(child, True, depth + 1)
            if score < best_score:
                best_score = score
                best_path = [node.sequence] + path
        if depth == 0:
            print(f"P2 MINIMAX Final Best Path: {' -> '.join(best_path)} | Score: {best_score}")
        return best_score, best_path


def minimax_alpha_beta(node, is_maximizing, depth=0, alpha=-float('inf'), beta=float('inf')):
    indent = "  " * depth

    if len(node.sequence) == 1:
        score = node.score_player1 - node.score_player2
        #print(f"{indent}Leaf Node: {node.sequence} | Score: {score}")
        return score, [node.sequence]

    if node.children is None:
        node.children = GameTree.generate_children(node)

    best_path = []

    if is_maximizing:
        max_eval = -float('inf')
        for child in node.children:
            eval, path = minimax_alpha_beta(child, False, depth + 1, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_path = [node.sequence] + path
            alpha = max(alpha, eval)
            if beta <= alpha:
                #print(f"{indent}PRUNE at MAX node: α={alpha}, β={beta}")
                break
        if depth == 0:
            print(f"P1 ALPHA_BETA Final Best Path: {' -> '.join(best_path)} | Score: {max_eval}")
        return max_eval, best_path
    else:
        min_eval = float('inf')
        for child in node.children:
            eval, path = minimax_alpha_beta(child, True, depth + 1, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_path = [node.sequence] + path
            beta = min(beta, eval)
            if beta <= alpha:
                #print(f"{indent}PRUNE at MIN node: α={alpha}, β={beta}")
                break
        if depth == 0:
            print(f"P2 ALPHA_BETA Final Best Path: {' -> '.join(best_path)} | Score: {min_eval}")
        return min_eval, best_path


# ----- Run and time both algorithms -----
game = GameTree(11, 11)

# Alpha-Beta
start_alpha = time.time()
minimax_alpha_beta(game.root, True)
end_alpha = time.time()
print(f"⏱️ Alpha-Beta Time: {end_alpha - start_alpha:.4f} seconds\n")

# Plain Minimax
start_plain = time.time()
minimax(game.root, True)
end_plain = time.time()
print(f"⏱ Plain Minimax Time: {end_plain - start_plain:.4f} seconds\n")
