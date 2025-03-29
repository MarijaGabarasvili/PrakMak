def transform_label(label: str) -> str:
    """
    Transform a label from the format:
      "Seq: 00100 | Score (P1:P2): 0:0 |"
    to a compact format:
      "0 | 00100 | 0"
    where the first number is player 1's score,
    the sequence is the series of 1's and 0's,
    and the last number is player 2's score.
    """
    parts = label.split("|")
    if len(parts) < 2:
        return label.strip()

    seq_part = parts[0].strip()
    score_part = parts[1].strip()

    # Remove the "Seq:" prefix
    if seq_part.startswith("Seq:"):
        seq = seq_part[len("Seq:"):].strip()
    else:
        seq = seq_part

    # Remove the "Score (P1:P2):" prefix
    if score_part.startswith("Score (P1:P2):"):
        score = score_part[len("Score (P1:P2):"):].strip()
    else:
        score = score_part

    scores = score.split(":")
    if len(scores) != 2:
        return f"{score} | {seq} | "
    p1, p2 = scores
    return f"{p1} | {seq} | {p2}"

def parse_game_tree(tree_str):
    """
    Parses an ASCII tree into a list of edges and transformed node labels.
    Each line with a node is assumed to contain either "└──" or "├──".
    The index of the marker is used as a proxy for the node's depth.
    Returns a list of edges (parent_label, child_label) and a list of transformed node labels.
    """
    edges = []
    nodes = []
    stack = []  # Each element is a tuple (depth, label)
    
    for line in tree_str.splitlines():
        if not line.strip():
            continue

        # Check for node marker.
        if "└──" in line:
            marker = "└──"
        elif "├──" in line:
            marker = "├──"
        else:
            continue

        marker_index = line.index(marker)
        raw_label = line[marker_index + len(marker):].strip()
        # Transform the label to the compact "xx | y...y | zz" form.
        label = transform_label(raw_label)
        current_depth = marker_index

        nodes.append(label)

        # Find parent node using the current depth.
        while stack and stack[-1][0] >= current_depth:
            stack.pop()
        if stack:
            parent_label = stack[-1][1]
            edges.append((parent_label, label))
        stack.append((current_depth, label))
    
    return edges, nodes

def generate_mermaid(edges, nodes):
    """
    Generates Mermaid diagram code using the given edges and node labels.
    Nodes with identical labels are merged.
    The diagram header "graph LR" ensures a left-to-right layout (straight links).
    Duplicate edges are removed.
    """
    # Create a unique set of nodes (by label).
    unique_nodes = set(nodes)
    # Map each unique node label to a unique ID.
    label_to_id = {label: f"node{i}" for i, label in enumerate(unique_nodes)}
    
    mermaid_lines = ["graph TD"]
    
    # Define each unique node.
    for label, node_id in label_to_id.items():
        mermaid_lines.append(f'{node_id}["{label}"]')
    
    # Remove duplicate edges.
    unique_edges = set()
    for parent, child in edges:
        parent_id = label_to_id[parent]
        child_id = label_to_id[child]
        unique_edges.add((parent_id, child_id))
    
    # Add deduplicated edges.
    for parent_id, child_id in unique_edges:
        mermaid_lines.append(f"{parent_id} --> {child_id}")
    
    return "\n".join(mermaid_lines)

if __name__ == "__main__":
    tree_str = r"""
└── Seq: 1010101 | Score (P1:P2): 0:0 |
        ├── Seq: 110101 | Score (P1:P2): -1:0 |
        │       ├── Seq: 00101 | Score (P1:P2): -1:1 |
        │       │       ├── Seq: 1101 | Score (P1:P2): 0:1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): 0:2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): 1:2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:3 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:3 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): 1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │       │       └── Seq: 110 | Score (P1:P2): 0:0 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): 1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): 1:1 | 
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       ├── Seq: 0001 | Score (P1:P2): -2:1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): -2:2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -3:2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:3 |
        │       │       │       └── Seq: 000 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │               └── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 0011 | Score (P1:P2): -2:1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │       │       └── Seq: 000 | Score (P1:P2): -2:2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -1:2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │               └── Seq: 01 | Score (P1:P2): -1:2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       └── Seq: 0010 | Score (P1:P2): -2:1 |
        │       │               ├── Seq: 110 | Score (P1:P2): -2:2 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): -1:2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:3 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -3:2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -3:3 |
        │       │               ├── Seq: 000 | Score (P1:P2): -2:0 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -1:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │               │       └── Seq: 01 | Score (P1:P2): -1:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │               └── Seq: 001 | Score (P1:P2): -2:0 |
        │       │                       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │                       └── Seq: 00 | Score (P1:P2): -3:0 |
        │       │                               └── Seq: 1 | Score (P1:P2): -3:1 |
        │       ├── Seq: 11101 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 0101 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): 1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): 1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │       │       └── Seq: 010 | Score (P1:P2): 0:-2 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │               └── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       ├── Seq: 1001 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): 1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): 0:-2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │               └── Seq: 11 | Score (P1:P2): 1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       ├── Seq: 1111 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -3:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       └── Seq: 1110 | Score (P1:P2): -2:-1 |
        │       │               ├── Seq: 010 | Score (P1:P2): -2:0 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): -3:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │               │       └── Seq: 01 | Score (P1:P2): -3:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │               ├── Seq: 100 | Score (P1:P2): -2:0 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -3:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │               └── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │                       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │                       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │                               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       ├── Seq: 11001 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 0001 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │       │       └── Seq: 000 | Score (P1:P2): 0:-2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): 1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): 1:-3 |
        │       │       │               └── Seq: 01 | Score (P1:P2): 1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): 1:-3 |
        │       │       ├── Seq: 1101 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       ├── Seq: 1111 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       └── Seq: 110 | Score (P1:P2): 0:0 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): 1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       └── Seq: 1100 | Score (P1:P2): -2:-1 |
        │       │               ├── Seq: 000 | Score (P1:P2): -2:0 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -1:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │               │       └── Seq: 01 | Score (P1:P2): -1:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │               ├── Seq: 110 | Score (P1:P2): -2:-2 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │               └── Seq: 111 | Score (P1:P2): -2:0 |
        │       │                       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │                       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │                               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       ├── Seq: 11011 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 0011 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): 1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): 1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:-2 | 
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       └── Seq: 000 | Score (P1:P2): 0:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): 1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │       │               └── Seq: 01 | Score (P1:P2): 1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       ├── Seq: 1111 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -3:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       ├── Seq: 1101 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       └── Seq: 1100 | Score (P1:P2): 0:-1 |
        │       │               ├── Seq: 000 | Score (P1:P2): 0:0 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): 1:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │               │       └── Seq: 01 | Score (P1:P2): 1:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │               ├── Seq: 110 | Score (P1:P2): 0:-2 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): 1:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │               └── Seq: 111 | Score (P1:P2): 0:0 |
        │       │                       ├── Seq: 01 | Score (P1:P2): 1:0 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │                       └── Seq: 10 | Score (P1:P2): 1:0 |
        │       │                               └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       └── Seq: 11010 | Score (P1:P2): -1:-1 |
        │               ├── Seq: 0010 | Score (P1:P2): 0:-1 |
        │               │       ├── Seq: 110 | Score (P1:P2): 0:0 |
        │               │       │       ├── Seq: 00 | Score (P1:P2): 1:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): 1:1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -1:0 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -1:1 |
        │               │       ├── Seq: 000 | Score (P1:P2): 0:-2 |
        │               │       │       ├── Seq: 10 | Score (P1:P2): 1:-2 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): 1:-3 |
        │               │       │       └── Seq: 01 | Score (P1:P2): 1:-2 |
        │               │       │               └── Seq: 0 | Score (P1:P2): 1:-3 |
        │               │       └── Seq: 001 | Score (P1:P2): 0:-2 |
        │               │               ├── Seq: 11 | Score (P1:P2): 1:-2 |
        │               │               │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │               │               └── Seq: 00 | Score (P1:P2): -1:-2 |
        │               │                       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │               ├── Seq: 1110 | Score (P1:P2): -2:-1 |
        │               │       ├── Seq: 010 | Score (P1:P2): -2:0 |
        │               │       │       ├── Seq: 00 | Score (P1:P2): -3:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -3:1 |
        │               │       │       └── Seq: 01 | Score (P1:P2): -3:0 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -3:-1 |
        │               │       ├── Seq: 100 | Score (P1:P2): -2:0 |
        │               │       │       ├── Seq: 10 | Score (P1:P2): -3:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -1:0 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -1:1 |
        │               │       └── Seq: 111 | Score (P1:P2): -2:-2 |
        │               │               ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │               │               │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │               │               └── Seq: 10 | Score (P1:P2): -1:-2 |
        │               │                       └── Seq: 1 | Score (P1:P2): -1:-3 |
        │               ├── Seq: 1100 | Score (P1:P2): -2:-1 |
        │               │       ├── Seq: 000 | Score (P1:P2): -2:0 |
        │               │       │       ├── Seq: 10 | Score (P1:P2): -1:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │               │       │       └── Seq: 01 | Score (P1:P2): -1:0 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │               │       ├── Seq: 110 | Score (P1:P2): -2:-2 |
        │               │       │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -3:-2 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -3:-1 |
        │               │       └── Seq: 111 | Score (P1:P2): -2:0 |
        │               │               ├── Seq: 01 | Score (P1:P2): -1:0 |
        │               │               │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │               │               └── Seq: 10 | Score (P1:P2): -1:0 |
        │               │                       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │               └── Seq: 1101 | Score (P1:P2): -2:-1 |
        │                       ├── Seq: 001 | Score (P1:P2): -2:0 |
        │                       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │                       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │                       │       └── Seq: 00 | Score (P1:P2): -3:0 |
        │                       │               └── Seq: 1 | Score (P1:P2): -3:1 |
        │                       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │                       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │                       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │                       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │                       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │                       └── Seq: 110 | Score (P1:P2): -2:-2 |
        │                               ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │                               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │                               └── Seq: 11 | Score (P1:P2): -3:-2 |
        │                                       └── Seq: 0 | Score (P1:P2): -3:-1 |
        ├── Seq: 100101 | Score (P1:P2): -1:0 |
        │       ├── Seq: 10101 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1101 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       ├── Seq: 1001 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1011 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       └── Seq: 1010 | Score (P1:P2): -2:-1 |
        │       │               ├── Seq: 110 | Score (P1:P2): -2:-2 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │               ├── Seq: 100 | Score (P1:P2): -2:-2 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:-1 | 
        │       │               └── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │                       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │                       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │                               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       ├── Seq: 11101 | Score (P1:P2): -1:1 |
        │       │       ├── Seq: 0101 | Score (P1:P2): 0:1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): 1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │       │       └── Seq: 010 | Score (P1:P2): 0:0 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │               └── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1001 | Score (P1:P2): 0:1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): 0:2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): 1:2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): 1:2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): 0:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): 1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): 1:1 |
        │       │       ├── Seq: 1111 | Score (P1:P2): -2:1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): -2:2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -3:2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:3 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:2 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:3 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:3 |
        │       │       └── Seq: 1110 | Score (P1:P2): -2:1 |
        │       │               ├── Seq: 010 | Score (P1:P2): -2:2 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): -3:2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -3:3 |
        │       │               │       └── Seq: 01 | Score (P1:P2): -3:2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │               ├── Seq: 100 | Score (P1:P2): -2:2 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -3:2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:3 |
        │       │               └── Seq: 111 | Score (P1:P2): -2:0 |
        │       │                       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │                       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │                               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       ├── Seq: 10001 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1001 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1101 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): 1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): 1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): 1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:-3 |
        │       │       │       └── Seq: 110 | Score (P1:P2): 0:-2 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): 1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1011 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): 1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): 1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:-3 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       └── Seq: 100 | Score (P1:P2): 0:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): 1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): 1:1 |
        │       │       └── Seq: 1000 | Score (P1:P2): -2:-1 |
        │       │               ├── Seq: 100 | Score (P1:P2): -2:-2 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │               ├── Seq: 110 | Score (P1:P2): -2:0 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): -1:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -3:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │               └── Seq: 101 | Score (P1:P2): -2:0 |
        │       │                       ├── Seq: 11 | Score (P1:P2): -3:0 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │                       └── Seq: 10 | Score (P1:P2): -3:0 |
        │       │                               └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       ├── Seq: 10011 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1011 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       ├── Seq: 1111 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 | 
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       └── Seq: 110 | Score (P1:P2): 0:0 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): 1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       ├── Seq: 1001 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       └── Seq: 1000 | Score (P1:P2): 0:-1 |
        │       │               ├── Seq: 100 | Score (P1:P2): 0:-2 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │               │       └── Seq: 11 | Score (P1:P2): 1:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │               ├── Seq: 110 | Score (P1:P2): 0:0 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): 1:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │               └── Seq: 101 | Score (P1:P2): 0:0 |
        │       │                       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │                       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │                               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       └── Seq: 10010 | Score (P1:P2): -1:-1 |
        │               ├── Seq: 1010 | Score (P1:P2): -2:-1 |
        │               │       ├── Seq: 110 | Score (P1:P2): -2:-2 |
        │               │       │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -3:-2 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -3:-1 |
        │               │       ├── Seq: 100 | Score (P1:P2): -2:-2 |
        │               │       │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -1:-2 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │               │       └── Seq: 101 | Score (P1:P2): -2:-2 |
        │               │               ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │               │               │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │               │               └── Seq: 10 | Score (P1:P2): -3:-2 |
        │               │                       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │               ├── Seq: 1110 | Score (P1:P2): 0:-1 |
        │               │       ├── Seq: 010 | Score (P1:P2): 0:0 |
        │               │       │       ├── Seq: 00 | Score (P1:P2): -1:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │               │       │       └── Seq: 01 | Score (P1:P2): -1:0 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │               │       ├── Seq: 100 | Score (P1:P2): 0:0 |
        │               │       │       ├── Seq: 10 | Score (P1:P2): -1:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): 1:0 |
        │               │       │               └── Seq: 0 | Score (P1:P2): 1:1 |
        │               │       └── Seq: 111 | Score (P1:P2): 0:-2 |
        │               │               ├── Seq: 01 | Score (P1:P2): 1:-2 |
        │               │               │       └── Seq: 0 | Score (P1:P2): 1:-3 |
        │               │               └── Seq: 10 | Score (P1:P2): 1:-2 |
        │               │                       └── Seq: 1 | Score (P1:P2): 1:-3 |
        │               ├── Seq: 1000 | Score (P1:P2): -2:-1 |
        │               │       ├── Seq: 100 | Score (P1:P2): -2:-2 |
        │               │       │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -1:-2 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │               │       ├── Seq: 110 | Score (P1:P2): -2:0 |
        │               │       │       ├── Seq: 00 | Score (P1:P2): -1:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -3:0 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -3:1 |
        │               │       └── Seq: 101 | Score (P1:P2): -2:0 |
        │               │               ├── Seq: 11 | Score (P1:P2): -3:0 |
        │               │               │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │               │               └── Seq: 10 | Score (P1:P2): -3:0 |
        │               │                       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │               └── Seq: 1001 | Score (P1:P2): -2:-1 |
        │                       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │                       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │                       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │                       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │                       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │                       ├── Seq: 111 | Score (P1:P2): -2:0 |
        │                       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │                       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │                       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │                       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │                       └── Seq: 100 | Score (P1:P2): -2:-2 |
        │                               ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │                               │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │                               └── Seq: 11 | Score (P1:P2): -1:-2 |
        │                                       └── Seq: 0 | Score (P1:P2): -1:-1 |
        ├── Seq: 101101 | Score (P1:P2): -1:0 |
        │       ├── Seq: 11101 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 0101 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): 1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): 1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │       │       └── Seq: 010 | Score (P1:P2): 0:-2 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │               └── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       ├── Seq: 1001 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): 1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): 0:-2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │               └── Seq: 11 | Score (P1:P2): 1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       ├── Seq: 1111 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -3:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       └── Seq: 1110 | Score (P1:P2): -2:-1 |
        │       │               ├── Seq: 010 | Score (P1:P2): -2:0 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): -3:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │               │       └── Seq: 01 | Score (P1:P2): -3:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │               ├── Seq: 100 | Score (P1:P2): -2:0 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -3:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │               └── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │                       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │                       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │                               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       ├── Seq: 10101 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1101 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       ├── Seq: 1001 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1011 | Score (P1:P2): -2:-1 | 
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       └── Seq: 1010 | Score (P1:P2): -2:-1 |
        │       │               ├── Seq: 110 | Score (P1:P2): -2:-2 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │               ├── Seq: 100 | Score (P1:P2): -2:-2 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │               └── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │                       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │                       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │                               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       ├── Seq: 10001 | Score (P1:P2): -1:1 |
        │       │       ├── Seq: 1001 | Score (P1:P2): -2:1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       ├── Seq: 1101 | Score (P1:P2): 0:1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): 0:2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): 1:2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:3 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:3 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): 1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │       │       └── Seq: 110 | Score (P1:P2): 0:0 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): 1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       ├── Seq: 1011 | Score (P1:P2): 0:1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): 1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): 0:2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -1:2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): 1:2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): 1:3 |
        │       │       └── Seq: 1000 | Score (P1:P2): -2:1 |
        │       │               ├── Seq: 100 | Score (P1:P2): -2:0 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -3:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │               ├── Seq: 110 | Score (P1:P2): -2:2 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): -1:2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:3 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -3:2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -3:3 |
        │       │               └── Seq: 101 | Score (P1:P2): -2:2 |
        │       │                       ├── Seq: 11 | Score (P1:P2): -3:2 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -3:3 |
        │       │                       └── Seq: 10 | Score (P1:P2): -3:2 |
        │       │                               └── Seq: 1 | Score (P1:P2): -3:1 |
        │       ├── Seq: 10111 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1111 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -3:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       ├── Seq: 1011 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       ├── Seq: 1001 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): 1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): 0:-2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │               └── Seq: 11 | Score (P1:P2): 1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       └── Seq: 1010 | Score (P1:P2): 0:-1 |
        │       │               ├── Seq: 110 | Score (P1:P2): 0:-2 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): 1:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │               ├── Seq: 100 | Score (P1:P2): 0:-2 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │               │       └── Seq: 11 | Score (P1:P2): 1:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │               └── Seq: 101 | Score (P1:P2): 0:-2 |
        │       │                       ├── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │                       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │                               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       └── Seq: 10110 | Score (P1:P2): -1:-1 |
        │               ├── Seq: 1110 | Score (P1:P2): -2:-1 |
        │               │       ├── Seq: 010 | Score (P1:P2): -2:0 |
        │               │       │       ├── Seq: 00 | Score (P1:P2): -3:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -3:1 |
        │               │       │       └── Seq: 01 | Score (P1:P2): -3:0 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -3:-1 |
        │               │       ├── Seq: 100 | Score (P1:P2): -2:0 |
        │               │       │       ├── Seq: 10 | Score (P1:P2): -3:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -1:0 | 
        │               │       │               └── Seq: 0 | Score (P1:P2): -1:1 |
        │               │       └── Seq: 111 | Score (P1:P2): -2:-2 |
        │               │               ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │               │               │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │               │               └── Seq: 10 | Score (P1:P2): -1:-2 |
        │               │                       └── Seq: 1 | Score (P1:P2): -1:-3 |
        │               ├── Seq: 1010 | Score (P1:P2): -2:-1 |
        │               │       ├── Seq: 110 | Score (P1:P2): -2:-2 |
        │               │       │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -3:-2 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -3:-1 |
        │               │       ├── Seq: 100 | Score (P1:P2): -2:-2 |
        │               │       │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -1:-2 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │               │       └── Seq: 101 | Score (P1:P2): -2:-2 |
        │               │               ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │               │               │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │               │               └── Seq: 10 | Score (P1:P2): -3:-2 |
        │               │                       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │               ├── Seq: 1000 | Score (P1:P2): 0:-1 |
        │               │       ├── Seq: 100 | Score (P1:P2): 0:-2 |
        │               │       │       ├── Seq: 10 | Score (P1:P2): -1:-2 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:-3 |
        │               │       │       └── Seq: 11 | Score (P1:P2): 1:-2 |
        │               │       │               └── Seq: 0 | Score (P1:P2): 1:-1 |
        │               │       ├── Seq: 110 | Score (P1:P2): 0:0 |
        │               │       │       ├── Seq: 00 | Score (P1:P2): 1:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): 1:1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -1:0 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -1:1 |
        │               │       └── Seq: 101 | Score (P1:P2): 0:0 |
        │               │               ├── Seq: 11 | Score (P1:P2): -1:0 |
        │               │               │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │               │               └── Seq: 10 | Score (P1:P2): -1:0 |
        │               │                       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │               └── Seq: 1011 | Score (P1:P2): -2:-1 |
        │                       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │                       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │                       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │                       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │                       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │                       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │                       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │                       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │                       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │                       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │                       └── Seq: 100 | Score (P1:P2): -2:0 |
        │                               ├── Seq: 10 | Score (P1:P2): -3:0 |
        │                               │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │                               └── Seq: 11 | Score (P1:P2): -1:0 |
        │                                       └── Seq: 0 | Score (P1:P2): -1:1 |
        ├── Seq: 101001 | Score (P1:P2): -1:0 |
        │       ├── Seq: 11001 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 0001 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │       │       └── Seq: 000 | Score (P1:P2): 0:-2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): 1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): 1:-3 |
        │       │       │               └── Seq: 01 | Score (P1:P2): 1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): 1:-3 |
        │       │       ├── Seq: 1101 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       ├── Seq: 1111 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       └── Seq: 110 | Score (P1:P2): 0:0 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): 1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       └── Seq: 1100 | Score (P1:P2): -2:-1 |
        │       │               ├── Seq: 000 | Score (P1:P2): -2:0 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -1:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │               │       └── Seq: 01 | Score (P1:P2): -1:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │               ├── Seq: 110 | Score (P1:P2): -2:-2 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │               └── Seq: 111 | Score (P1:P2): -2:0 |
        │       │                       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │                       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │                               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       ├── Seq: 10001 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1001 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1101 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): 1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): 1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): 1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:-3 |
        │       │       │       └── Seq: 110 | Score (P1:P2): 0:-2 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): 1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1011 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): 1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): 1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:-3 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       └── Seq: 100 | Score (P1:P2): 0:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): 1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): 1:1 |
        │       │       └── Seq: 1000 | Score (P1:P2): -2:-1 |
        │       │               ├── Seq: 100 | Score (P1:P2): -2:-2 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │               ├── Seq: 110 | Score (P1:P2): -2:0 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): -1:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:1 | 
        │       │               │       └── Seq: 11 | Score (P1:P2): -3:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │               └── Seq: 101 | Score (P1:P2): -2:0 |
        │       │                       ├── Seq: 11 | Score (P1:P2): -3:0 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │                       └── Seq: 10 | Score (P1:P2): -3:0 |
        │       │                               └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       ├── Seq: 10101 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1101 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       ├── Seq: 1001 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1011 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       └── Seq: 1010 | Score (P1:P2): -2:-1 |
        │       │               ├── Seq: 110 | Score (P1:P2): -2:-2 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │               ├── Seq: 100 | Score (P1:P2): -2:-2 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │               └── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │                       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │                       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │                               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       ├── Seq: 10111 | Score (P1:P2): -1:1 |
        │       │       ├── Seq: 1111 | Score (P1:P2): -2:1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): -2:2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -3:2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:3 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:2 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:3 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:3 |
        │       │       ├── Seq: 1011 | Score (P1:P2): -2:1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:3 |
        │       │       ├── Seq: 1001 | Score (P1:P2): 0:1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): 0:2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): 1:2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): 1:2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): 0:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): 1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): 1:1 |
        │       │       └── Seq: 1010 | Score (P1:P2): 0:1 |
        │       │               ├── Seq: 110 | Score (P1:P2): 0:0 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): 1:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │               ├── Seq: 100 | Score (P1:P2): 0:0 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -1:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): 1:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): 1:1 |
        │       │               └── Seq: 101 | Score (P1:P2): 0:0 |
        │       │                       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │                       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │                               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       └── Seq: 10100 | Score (P1:P2): -1:-1 |
        │               ├── Seq: 1100 | Score (P1:P2): -2:-1 |
        │               │       ├── Seq: 000 | Score (P1:P2): -2:0 |
        │               │       │       ├── Seq: 10 | Score (P1:P2): -1:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │               │       │       └── Seq: 01 | Score (P1:P2): -1:0 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │               │       ├── Seq: 110 | Score (P1:P2): -2:-2 |
        │               │       │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -3:-2 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -3:-1 |
        │               │       └── Seq: 111 | Score (P1:P2): -2:0 |
        │               │               ├── Seq: 01 | Score (P1:P2): -1:0 |
        │               │               │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │               │               └── Seq: 10 | Score (P1:P2): -1:0 |
        │               │                       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │               ├── Seq: 1000 | Score (P1:P2): -2:-1 |
        │               │       ├── Seq: 100 | Score (P1:P2): -2:-2 |
        │               │       │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -1:-2 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │               │       ├── Seq: 110 | Score (P1:P2): -2:0 |
        │               │       │       ├── Seq: 00 | Score (P1:P2): -1:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -3:0 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -3:1 |
        │               │       └── Seq: 101 | Score (P1:P2): -2:0 |
        │               │               ├── Seq: 11 | Score (P1:P2): -3:0 |
        │               │               │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │               │               └── Seq: 10 | Score (P1:P2): -3:0 |
        │               │                       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │               ├── Seq: 1010 | Score (P1:P2): -2:-1 |
        │               │       ├── Seq: 110 | Score (P1:P2): -2:-2 |
        │               │       │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -3:-2 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -3:-1 |
        │               │       ├── Seq: 100 | Score (P1:P2): -2:-2 |
        │               │       │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -1:-2 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │               │       └── Seq: 101 | Score (P1:P2): -2:-2 |
        │               │               ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │               │               │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │               │               └── Seq: 10 | Score (P1:P2): -3:-2 |
        │               │                       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │               └── Seq: 1011 | Score (P1:P2): 0:-1 |
        │                       ├── Seq: 111 | Score (P1:P2): 0:-2 |
        │                       │       ├── Seq: 01 | Score (P1:P2): 1:-2 |
        │                       │       │       └── Seq: 0 | Score (P1:P2): 1:-3 | 
        │                       │       └── Seq: 10 | Score (P1:P2): 1:-2 |
        │                       │               └── Seq: 1 | Score (P1:P2): 1:-3 |
        │                       ├── Seq: 101 | Score (P1:P2): 0:-2 |
        │                       │       ├── Seq: 11 | Score (P1:P2): -1:-2 |
        │                       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │                       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │                       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │                       └── Seq: 100 | Score (P1:P2): 0:0 |
        │                               ├── Seq: 10 | Score (P1:P2): -1:0 |
        │                               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │                               └── Seq: 11 | Score (P1:P2): 1:0 |
        │                                       └── Seq: 0 | Score (P1:P2): 1:1 |
        ├── Seq: 101011 | Score (P1:P2): -1:0 |
        │       ├── Seq: 11011 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 0011 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): 1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): 1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       └── Seq: 000 | Score (P1:P2): 0:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): 1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │       │               └── Seq: 01 | Score (P1:P2): 1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       ├── Seq: 1111 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -3:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       ├── Seq: 1101 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       └── Seq: 1100 | Score (P1:P2): 0:-1 |
        │       │               ├── Seq: 000 | Score (P1:P2): 0:0 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): 1:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │               │       └── Seq: 01 | Score (P1:P2): 1:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │               ├── Seq: 110 | Score (P1:P2): 0:-2 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): 1:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │               └── Seq: 111 | Score (P1:P2): 0:0 |
        │       │                       ├── Seq: 01 | Score (P1:P2): 1:0 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │                       └── Seq: 10 | Score (P1:P2): 1:0 |
        │       │                               └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       ├── Seq: 10011 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1011 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       ├── Seq: 1111 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       └── Seq: 110 | Score (P1:P2): 0:0 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): 1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       ├── Seq: 1001 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       └── Seq: 1000 | Score (P1:P2): 0:-1 |
        │       │               ├── Seq: 100 | Score (P1:P2): 0:-2 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │               │       └── Seq: 11 | Score (P1:P2): 1:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │               ├── Seq: 110 | Score (P1:P2): 0:0 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): 1:0 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): 1:1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │               └── Seq: 101 | Score (P1:P2): 0:0 |
        │       │                       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │                       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │                               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       ├── Seq: 10111 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1111 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 011 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -3:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:1 |
        │       │       ├── Seq: 1011 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       ├── Seq: 1001 | Score (P1:P2): 0:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): 0:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): 0:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): 1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): 1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): 0:-2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-3 | 
        │       │       │               └── Seq: 11 | Score (P1:P2): 1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │       └── Seq: 1010 | Score (P1:P2): 0:-1 |
        │       │               ├── Seq: 110 | Score (P1:P2): 0:-2 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): 1:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): 1:-1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │               ├── Seq: 100 | Score (P1:P2): 0:-2 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │               │       └── Seq: 11 | Score (P1:P2): 1:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): 1:-1 |
        │       │               └── Seq: 101 | Score (P1:P2): 0:-2 |
        │       │                       ├── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │                       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │                               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       ├── Seq: 10101 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1101 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 001 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       │       │       └── Seq: 00 | Score (P1:P2): -3:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       └── Seq: 110 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       ├── Seq: 1001 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:0 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:-2 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │       ├── Seq: 1011 | Score (P1:P2): -2:-1 |
        │       │       │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
        │       │       │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │       │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │       │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │       │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │       │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │       │       └── Seq: 100 | Score (P1:P2): -2:0 |
        │       │       │               ├── Seq: 10 | Score (P1:P2): -3:0 |
        │       │       │               │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │       │       │               └── Seq: 11 | Score (P1:P2): -1:0 |
        │       │       │                       └── Seq: 0 | Score (P1:P2): -1:1 |
        │       │       └── Seq: 1010 | Score (P1:P2): -2:-1 |
        │       │               ├── Seq: 110 | Score (P1:P2): -2:-2 |
        │       │               │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │               ├── Seq: 100 | Score (P1:P2): -2:-2 |
        │       │               │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │               │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       │               │       └── Seq: 11 | Score (P1:P2): -1:-2 |
        │       │               │               └── Seq: 0 | Score (P1:P2): -1:-1 |
        │       │               └── Seq: 101 | Score (P1:P2): -2:-2 |
        │       │                       ├── Seq: 11 | Score (P1:P2): -3:-2 |
        │       │                       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
        │       │                       └── Seq: 10 | Score (P1:P2): -3:-2 |
        │       │                               └── Seq: 1 | Score (P1:P2): -3:-3 |
        │       └── Seq: 10100 | Score (P1:P2): -1:1 |
        │               ├── Seq: 1100 | Score (P1:P2): -2:1 |
        │               │       ├── Seq: 000 | Score (P1:P2): -2:2 |
        │               │       │       ├── Seq: 10 | Score (P1:P2): -1:2 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │               │       │       └── Seq: 01 | Score (P1:P2): -1:2 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -1:1 |
        │               │       ├── Seq: 110 | Score (P1:P2): -2:0 |
        │               │       │       ├── Seq: 00 | Score (P1:P2): -1:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -3:0 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -3:1 |
        │               │       └── Seq: 111 | Score (P1:P2): -2:2 |
        │               │               ├── Seq: 01 | Score (P1:P2): -1:2 |
        │               │               │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │               │               └── Seq: 10 | Score (P1:P2): -1:2 |
        │               │                       └── Seq: 1 | Score (P1:P2): -1:1 |
        │               ├── Seq: 1000 | Score (P1:P2): -2:1 |
        │               │       ├── Seq: 100 | Score (P1:P2): -2:0 |
        │               │       │       ├── Seq: 10 | Score (P1:P2): -3:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -1:0 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -1:1 |
        │               │       ├── Seq: 110 | Score (P1:P2): -2:2 |
        │               │       │       ├── Seq: 00 | Score (P1:P2): -1:2 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:3 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -3:2 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -3:3 |
        │               │       └── Seq: 101 | Score (P1:P2): -2:2 |
        │               │               ├── Seq: 11 | Score (P1:P2): -3:2 |
        │               │               │       └── Seq: 0 | Score (P1:P2): -3:3 |
        │               │               └── Seq: 10 | Score (P1:P2): -3:2 |
        │               │                       └── Seq: 1 | Score (P1:P2): -3:1 |
        │               ├── Seq: 1010 | Score (P1:P2): -2:1 |
        │               │       ├── Seq: 110 | Score (P1:P2): -2:0 |
        │               │       │       ├── Seq: 00 | Score (P1:P2): -1:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -3:0 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -3:1 |
        │               │       ├── Seq: 100 | Score (P1:P2): -2:0 |
        │               │       │       ├── Seq: 10 | Score (P1:P2): -3:0 |
        │               │       │       │       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │               │       │       └── Seq: 11 | Score (P1:P2): -1:0 |
        │               │       │               └── Seq: 0 | Score (P1:P2): -1:1 |
        │               │       └── Seq: 101 | Score (P1:P2): -2:0 |
        │               │               ├── Seq: 11 | Score (P1:P2): -3:0 |
        │               │               │       └── Seq: 0 | Score (P1:P2): -3:1 |
        │               │               └── Seq: 10 | Score (P1:P2): -3:0 |
        │               │                       └── Seq: 1 | Score (P1:P2): -3:-1 |
        │               └── Seq: 1011 | Score (P1:P2): 0:1 |
        │                       ├── Seq: 111 | Score (P1:P2): 0:0 |
        │                       │       ├── Seq: 01 | Score (P1:P2): 1:0 |
        │                       │       │       └── Seq: 0 | Score (P1:P2): 1:-1 |
        │                       │       └── Seq: 10 | Score (P1:P2): 1:0 |
        │                       │               └── Seq: 1 | Score (P1:P2): 1:-1 |
        │                       ├── Seq: 101 | Score (P1:P2): 0:0 |
        │                       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
        │                       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
        │                       │       └── Seq: 10 | Score (P1:P2): -1:0 |
        │                       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
        │                       └── Seq: 100 | Score (P1:P2): 0:2 |
        │                               ├── Seq: 10 | Score (P1:P2): -1:2 |
        │                               │       └── Seq: 1 | Score (P1:P2): -1:1 |
        │                               └── Seq: 11 | Score (P1:P2): 1:2 |
        │                                       └── Seq: 0 | Score (P1:P2): 1:3 |
        └── Seq: 101010 | Score (P1:P2): -1:0 |
                ├── Seq: 11010 | Score (P1:P2): -1:-1 |
                │       ├── Seq: 0010 | Score (P1:P2): 0:-1 |
                │       │       ├── Seq: 110 | Score (P1:P2): 0:0 |
                │       │       │       ├── Seq: 00 | Score (P1:P2): 1:0 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): 1:1 |
                │       │       │       └── Seq: 11 | Score (P1:P2): -1:0 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -1:1 |
                │       │       ├── Seq: 000 | Score (P1:P2): 0:-2 |
                │       │       │       ├── Seq: 10 | Score (P1:P2): 1:-2 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): 1:-3 |
                │       │       │       └── Seq: 01 | Score (P1:P2): 1:-2 |
                │       │       │               └── Seq: 0 | Score (P1:P2): 1:-3 |
                │       │       └── Seq: 001 | Score (P1:P2): 0:-2 |
                │       │               ├── Seq: 11 | Score (P1:P2): 1:-2 |
                │       │               │       └── Seq: 0 | Score (P1:P2): 1:-1 |
                │       │               └── Seq: 00 | Score (P1:P2): -1:-2 |
                │       │                       └── Seq: 1 | Score (P1:P2): -1:-1 |
                │       ├── Seq: 1110 | Score (P1:P2): -2:-1 |
                │       │       ├── Seq: 010 | Score (P1:P2): -2:0 |
                │       │       │       ├── Seq: 00 | Score (P1:P2): -3:0 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -3:1 |
                │       │       │       └── Seq: 01 | Score (P1:P2): -3:0 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -3:-1 |
                │       │       ├── Seq: 100 | Score (P1:P2): -2:0 |
                │       │       │       ├── Seq: 10 | Score (P1:P2): -3:0 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -3:-1 |
                │       │       │       └── Seq: 11 | Score (P1:P2): -1:0 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -1:1 |
                │       │       └── Seq: 111 | Score (P1:P2): -2:-2 |
                │       │               ├── Seq: 01 | Score (P1:P2): -1:-2 |
                │       │               │       └── Seq: 0 | Score (P1:P2): -1:-3 |
                │       │               └── Seq: 10 | Score (P1:P2): -1:-2 |
                │       │                       └── Seq: 1 | Score (P1:P2): -1:-3 |
                │       ├── Seq: 1100 | Score (P1:P2): -2:-1 |
                │       │       ├── Seq: 000 | Score (P1:P2): -2:0 |
                │       │       │       ├── Seq: 10 | Score (P1:P2): -1:0 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
                │       │       │       └── Seq: 01 | Score (P1:P2): -1:0 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
                │       │       ├── Seq: 110 | Score (P1:P2): -2:-2 |
                │       │       │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
                │       │       │       └── Seq: 11 | Score (P1:P2): -3:-2 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -3:-1 | 
                │       │       └── Seq: 111 | Score (P1:P2): -2:0 |
                │       │               ├── Seq: 01 | Score (P1:P2): -1:0 |
                │       │               │       └── Seq: 0 | Score (P1:P2): -1:-1 |
                │       │               └── Seq: 10 | Score (P1:P2): -1:0 |
                │       │                       └── Seq: 1 | Score (P1:P2): -1:-1 |
                │       └── Seq: 1101 | Score (P1:P2): -2:-1 |
                │               ├── Seq: 001 | Score (P1:P2): -2:0 |
                │               │       ├── Seq: 11 | Score (P1:P2): -1:0 |
                │               │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
                │               │       └── Seq: 00 | Score (P1:P2): -3:0 |
                │               │               └── Seq: 1 | Score (P1:P2): -3:1 |
                │               ├── Seq: 111 | Score (P1:P2): -2:-2 |
                │               │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
                │               │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
                │               │       └── Seq: 10 | Score (P1:P2): -1:-2 |
                │               │               └── Seq: 1 | Score (P1:P2): -1:-3 |
                │               └── Seq: 110 | Score (P1:P2): -2:-2 |
                │                       ├── Seq: 00 | Score (P1:P2): -1:-2 |
                │                       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
                │                       └── Seq: 11 | Score (P1:P2): -3:-2 |
                │                               └── Seq: 0 | Score (P1:P2): -3:-1 |
                ├── Seq: 10010 | Score (P1:P2): -1:-1 |
                │       ├── Seq: 1010 | Score (P1:P2): -2:-1 |
                │       │       ├── Seq: 110 | Score (P1:P2): -2:-2 |
                │       │       │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
                │       │       │       └── Seq: 11 | Score (P1:P2): -3:-2 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -3:-1 |
                │       │       ├── Seq: 100 | Score (P1:P2): -2:-2 |
                │       │       │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
                │       │       │       └── Seq: 11 | Score (P1:P2): -1:-2 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
                │       │       └── Seq: 101 | Score (P1:P2): -2:-2 |
                │       │               ├── Seq: 11 | Score (P1:P2): -3:-2 |
                │       │               │       └── Seq: 0 | Score (P1:P2): -3:-1 |
                │       │               └── Seq: 10 | Score (P1:P2): -3:-2 |
                │       │                       └── Seq: 1 | Score (P1:P2): -3:-3 |
                │       ├── Seq: 1110 | Score (P1:P2): 0:-1 |
                │       │       ├── Seq: 010 | Score (P1:P2): 0:0 |
                │       │       │       ├── Seq: 00 | Score (P1:P2): -1:0 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -1:1 |
                │       │       │       └── Seq: 01 | Score (P1:P2): -1:0 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
                │       │       ├── Seq: 100 | Score (P1:P2): 0:0 |
                │       │       │       ├── Seq: 10 | Score (P1:P2): -1:0 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
                │       │       │       └── Seq: 11 | Score (P1:P2): 1:0 |
                │       │       │               └── Seq: 0 | Score (P1:P2): 1:1 |
                │       │       └── Seq: 111 | Score (P1:P2): 0:-2 |
                │       │               ├── Seq: 01 | Score (P1:P2): 1:-2 |
                │       │               │       └── Seq: 0 | Score (P1:P2): 1:-3 |
                │       │               └── Seq: 10 | Score (P1:P2): 1:-2 |
                │       │                       └── Seq: 1 | Score (P1:P2): 1:-3 |
                │       ├── Seq: 1000 | Score (P1:P2): -2:-1 |
                │       │       ├── Seq: 100 | Score (P1:P2): -2:-2 |
                │       │       │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
                │       │       │       └── Seq: 11 | Score (P1:P2): -1:-2 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
                │       │       ├── Seq: 110 | Score (P1:P2): -2:0 |
                │       │       │       ├── Seq: 00 | Score (P1:P2): -1:0 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -1:1 |
                │       │       │       └── Seq: 11 | Score (P1:P2): -3:0 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -3:1 |
                │       │       └── Seq: 101 | Score (P1:P2): -2:0 |
                │       │               ├── Seq: 11 | Score (P1:P2): -3:0 |
                │       │               │       └── Seq: 0 | Score (P1:P2): -3:1 |
                │       │               └── Seq: 10 | Score (P1:P2): -3:0 |
                │       │                       └── Seq: 1 | Score (P1:P2): -3:-1 |
                │       └── Seq: 1001 | Score (P1:P2): -2:-1 |
                │               ├── Seq: 101 | Score (P1:P2): -2:-2 |
                │               │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
                │               │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
                │               │       └── Seq: 10 | Score (P1:P2): -3:-2 |
                │               │               └── Seq: 1 | Score (P1:P2): -3:-3 |
                │               ├── Seq: 111 | Score (P1:P2): -2:0 |
                │               │       ├── Seq: 01 | Score (P1:P2): -1:0 |
                │               │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
                │               │       └── Seq: 10 | Score (P1:P2): -1:0 |
                │               │               └── Seq: 1 | Score (P1:P2): -1:-1 |
                │               └── Seq: 100 | Score (P1:P2): -2:-2 |
                │                       ├── Seq: 10 | Score (P1:P2): -3:-2 |
                │                       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
                │                       └── Seq: 11 | Score (P1:P2): -1:-2 |
                │                               └── Seq: 0 | Score (P1:P2): -1:-1 |
                ├── Seq: 10110 | Score (P1:P2): -1:-1 |
                │       ├── Seq: 1110 | Score (P1:P2): -2:-1 |
                │       │       ├── Seq: 010 | Score (P1:P2): -2:0 |
                │       │       │       ├── Seq: 00 | Score (P1:P2): -3:0 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -3:1 |
                │       │       │       └── Seq: 01 | Score (P1:P2): -3:0 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -3:-1 |
                │       │       ├── Seq: 100 | Score (P1:P2): -2:0 |
                │       │       │       ├── Seq: 10 | Score (P1:P2): -3:0 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -3:-1 |
                │       │       │       └── Seq: 11 | Score (P1:P2): -1:0 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -1:1 |
                │       │       └── Seq: 111 | Score (P1:P2): -2:-2 |
                │       │               ├── Seq: 01 | Score (P1:P2): -1:-2 |
                │       │               │       └── Seq: 0 | Score (P1:P2): -1:-3 |
                │       │               └── Seq: 10 | Score (P1:P2): -1:-2 |
                │       │                       └── Seq: 1 | Score (P1:P2): -1:-3 |
                │       ├── Seq: 1010 | Score (P1:P2): -2:-1 |
                │       │       ├── Seq: 110 | Score (P1:P2): -2:-2 |
                │       │       │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
                │       │       │       └── Seq: 11 | Score (P1:P2): -3:-2 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -3:-1 |
                │       │       ├── Seq: 100 | Score (P1:P2): -2:-2 |
                │       │       │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
                │       │       │       └── Seq: 11 | Score (P1:P2): -1:-2 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
                │       │       └── Seq: 101 | Score (P1:P2): -2:-2 |
                │       │               ├── Seq: 11 | Score (P1:P2): -3:-2 |
                │       │               │       └── Seq: 0 | Score (P1:P2): -3:-1 |
                │       │               └── Seq: 10 | Score (P1:P2): -3:-2 |
                │       │                       └── Seq: 1 | Score (P1:P2): -3:-3 |
                │       ├── Seq: 1000 | Score (P1:P2): 0:-1 |
                │       │       ├── Seq: 100 | Score (P1:P2): 0:-2 |
                │       │       │       ├── Seq: 10 | Score (P1:P2): -1:-2 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -1:-3 |
                │       │       │       └── Seq: 11 | Score (P1:P2): 1:-2 |
                │       │       │               └── Seq: 0 | Score (P1:P2): 1:-1 |
                │       │       ├── Seq: 110 | Score (P1:P2): 0:0 |
                │       │       │       ├── Seq: 00 | Score (P1:P2): 1:0 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): 1:1 |
                │       │       │       └── Seq: 11 | Score (P1:P2): -1:0 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -1:1 |
                │       │       └── Seq: 101 | Score (P1:P2): 0:0 |
                │       │               ├── Seq: 11 | Score (P1:P2): -1:0 |
                │       │               │       └── Seq: 0 | Score (P1:P2): -1:1 |
                │       │               └── Seq: 10 | Score (P1:P2): -1:0 |
                │       │                       └── Seq: 1 | Score (P1:P2): -1:-1 |
                │       └── Seq: 1011 | Score (P1:P2): -2:-1 |
                │               ├── Seq: 111 | Score (P1:P2): -2:-2 |
                │               │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
                │               │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
                │               │       └── Seq: 10 | Score (P1:P2): -1:-2 |
                │               │               └── Seq: 1 | Score (P1:P2): -1:-3 |
                │               ├── Seq: 101 | Score (P1:P2): -2:-2 |
                │               │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
                │               │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
                │               │       └── Seq: 10 | Score (P1:P2): -3:-2 |
                │               │               └── Seq: 1 | Score (P1:P2): -3:-3 |
                │               └── Seq: 100 | Score (P1:P2): -2:0 |
                │                       ├── Seq: 10 | Score (P1:P2): -3:0 |
                │                       │       └── Seq: 1 | Score (P1:P2): -3:-1 |
                │                       └── Seq: 11 | Score (P1:P2): -1:0 |
                │                               └── Seq: 0 | Score (P1:P2): -1:1 |
                ├── Seq: 10100 | Score (P1:P2): -1:-1 |
                │       ├── Seq: 1100 | Score (P1:P2): -2:-1 |
                │       │       ├── Seq: 000 | Score (P1:P2): -2:0 |
                │       │       │       ├── Seq: 10 | Score (P1:P2): -1:0 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
                │       │       │       └── Seq: 01 | Score (P1:P2): -1:0 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
                │       │       ├── Seq: 110 | Score (P1:P2): -2:-2 |
                │       │       │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
                │       │       │       └── Seq: 11 | Score (P1:P2): -3:-2 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -3:-1 |
                │       │       └── Seq: 111 | Score (P1:P2): -2:0 |
                │       │               ├── Seq: 01 | Score (P1:P2): -1:0 |
                │       │               │       └── Seq: 0 | Score (P1:P2): -1:-1 |
                │       │               └── Seq: 10 | Score (P1:P2): -1:0 |
                │       │                       └── Seq: 1 | Score (P1:P2): -1:-1 |
                │       ├── Seq: 1000 | Score (P1:P2): -2:-1 |
                │       │       ├── Seq: 100 | Score (P1:P2): -2:-2 |
                │       │       │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
                │       │       │       └── Seq: 11 | Score (P1:P2): -1:-2 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
                │       │       ├── Seq: 110 | Score (P1:P2): -2:0 |
                │       │       │       ├── Seq: 00 | Score (P1:P2): -1:0 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -1:1 |
                │       │       │       └── Seq: 11 | Score (P1:P2): -3:0 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -3:1 |
                │       │       └── Seq: 101 | Score (P1:P2): -2:0 |
                │       │               ├── Seq: 11 | Score (P1:P2): -3:0 |
                │       │               │       └── Seq: 0 | Score (P1:P2): -3:1 |
                │       │               └── Seq: 10 | Score (P1:P2): -3:0 |
                │       │                       └── Seq: 1 | Score (P1:P2): -3:-1 |
                │       ├── Seq: 1010 | Score (P1:P2): -2:-1 |
                │       │       ├── Seq: 110 | Score (P1:P2): -2:-2 |
                │       │       │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
                │       │       │       └── Seq: 11 | Score (P1:P2): -3:-2 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -3:-1 |
                │       │       ├── Seq: 100 | Score (P1:P2): -2:-2 |
                │       │       │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
                │       │       │       │       └── Seq: 1 | Score (P1:P2): -3:-3 | 
                │       │       │       └── Seq: 11 | Score (P1:P2): -1:-2 |
                │       │       │               └── Seq: 0 | Score (P1:P2): -1:-1 |
                │       │       └── Seq: 101 | Score (P1:P2): -2:-2 |
                │       │               ├── Seq: 11 | Score (P1:P2): -3:-2 |
                │       │               │       └── Seq: 0 | Score (P1:P2): -3:-1 |
                │       │               └── Seq: 10 | Score (P1:P2): -3:-2 |
                │       │                       └── Seq: 1 | Score (P1:P2): -3:-3 |
                │       └── Seq: 1011 | Score (P1:P2): 0:-1 |
                │               ├── Seq: 111 | Score (P1:P2): 0:-2 |
                │               │       ├── Seq: 01 | Score (P1:P2): 1:-2 |
                │               │       │       └── Seq: 0 | Score (P1:P2): 1:-3 |
                │               │       └── Seq: 10 | Score (P1:P2): 1:-2 |
                │               │               └── Seq: 1 | Score (P1:P2): 1:-3 |
                │               ├── Seq: 101 | Score (P1:P2): 0:-2 |
                │               │       ├── Seq: 11 | Score (P1:P2): -1:-2 |
                │               │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
                │               │       └── Seq: 10 | Score (P1:P2): -1:-2 |
                │               │               └── Seq: 1 | Score (P1:P2): -1:-3 |
                │               └── Seq: 100 | Score (P1:P2): 0:0 |
                │                       ├── Seq: 10 | Score (P1:P2): -1:0 |
                │                       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
                │                       └── Seq: 11 | Score (P1:P2): 1:0 |
                │                               └── Seq: 0 | Score (P1:P2): 1:1 |
                └── Seq: 10101 | Score (P1:P2): -1:-1 |
                        ├── Seq: 1101 | Score (P1:P2): -2:-1 |
                        │       ├── Seq: 001 | Score (P1:P2): -2:0 |
                        │       │       ├── Seq: 11 | Score (P1:P2): -1:0 |
                        │       │       │       └── Seq: 0 | Score (P1:P2): -1:1 |
                        │       │       └── Seq: 00 | Score (P1:P2): -3:0 |
                        │       │               └── Seq: 1 | Score (P1:P2): -3:1 |
                        │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
                        │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
                        │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
                        │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
                        │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
                        │       └── Seq: 110 | Score (P1:P2): -2:-2 |
                        │               ├── Seq: 00 | Score (P1:P2): -1:-2 |
                        │               │       └── Seq: 1 | Score (P1:P2): -1:-1 |
                        │               └── Seq: 11 | Score (P1:P2): -3:-2 |
                        │                       └── Seq: 0 | Score (P1:P2): -3:-1 |
                        ├── Seq: 1001 | Score (P1:P2): -2:-1 |
                        │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
                        │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
                        │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
                        │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
                        │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
                        │       ├── Seq: 111 | Score (P1:P2): -2:0 |
                        │       │       ├── Seq: 01 | Score (P1:P2): -1:0 |
                        │       │       │       └── Seq: 0 | Score (P1:P2): -1:-1 |
                        │       │       └── Seq: 10 | Score (P1:P2): -1:0 |
                        │       │               └── Seq: 1 | Score (P1:P2): -1:-1 |
                        │       └── Seq: 100 | Score (P1:P2): -2:-2 |
                        │               ├── Seq: 10 | Score (P1:P2): -3:-2 |
                        │               │       └── Seq: 1 | Score (P1:P2): -3:-3 |
                        │               └── Seq: 11 | Score (P1:P2): -1:-2 |
                        │                       └── Seq: 0 | Score (P1:P2): -1:-1 |
                        ├── Seq: 1011 | Score (P1:P2): -2:-1 |
                        │       ├── Seq: 111 | Score (P1:P2): -2:-2 |
                        │       │       ├── Seq: 01 | Score (P1:P2): -1:-2 |
                        │       │       │       └── Seq: 0 | Score (P1:P2): -1:-3 |
                        │       │       └── Seq: 10 | Score (P1:P2): -1:-2 |
                        │       │               └── Seq: 1 | Score (P1:P2): -1:-3 |
                        │       ├── Seq: 101 | Score (P1:P2): -2:-2 |
                        │       │       ├── Seq: 11 | Score (P1:P2): -3:-2 |
                        │       │       │       └── Seq: 0 | Score (P1:P2): -3:-1 |
                        │       │       └── Seq: 10 | Score (P1:P2): -3:-2 |
                        │       │               └── Seq: 1 | Score (P1:P2): -3:-3 |
                        │       └── Seq: 100 | Score (P1:P2): -2:0 |
                        │               ├── Seq: 10 | Score (P1:P2): -3:0 |
                        │               │       └── Seq: 1 | Score (P1:P2): -3:-1 |
                        │               └── Seq: 11 | Score (P1:P2): -1:0 |
                        │                       └── Seq: 0 | Score (P1:P2): -1:1 |
                        └── Seq: 1010 | Score (P1:P2): -2:-1 |
                                ├── Seq: 110 | Score (P1:P2): -2:-2 |
                                │       ├── Seq: 00 | Score (P1:P2): -1:-2 |
                                │       │       └── Seq: 1 | Score (P1:P2): -1:-1 |
                                │       └── Seq: 11 | Score (P1:P2): -3:-2 |
                                │               └── Seq: 0 | Score (P1:P2): -3:-1 |
                                ├── Seq: 100 | Score (P1:P2): -2:-2 |
                                │       ├── Seq: 10 | Score (P1:P2): -3:-2 |
                                │       │       └── Seq: 1 | Score (P1:P2): -3:-3 |
                                │       └── Seq: 11 | Score (P1:P2): -1:-2 |
                                │               └── Seq: 0 | Score (P1:P2): -1:-1 |
                                └── Seq: 101 | Score (P1:P2): -2:-2 |
                                        ├── Seq: 11 | Score (P1:P2): -3:-2 |
                                        │       └── Seq: 0 | Score (P1:P2): -3:-1 |
                                        └── Seq: 10 | Score (P1:P2): -3:-2 |
                                                └── Seq: 1 | Score (P1:P2): -3:-3 |
    """

    edges, nodes = parse_game_tree(tree_str)
    mermaid_code = generate_mermaid(edges, nodes)
    print(mermaid_code)
