from IPython import get_ipython
from anytree import Node, RenderTree
import copy

# Clear the Spyder console on script startup
get_ipython().magic('clear')
print("Konsole attīrīta. Spēle var sākties.")

input_pos1 = -69
input_pos2 = -69
player = 0

sakuma_sekvence = str("1101001001")
sekvence = list(sakuma_sekvence)
scores = [0,0]
    
# Game mode selection
mode = input("Izvēlies režīmu (PVP/PVC): ").strip().upper()
while mode not in ["PVP", "PVC"]:
    mode = input("Nepareiza izvēle, izvēlies: (PVP/PVC): ").strip().upper()

# Initialize an empty game tree
root = Node(f"{''.join(sekvence)}")
last_node = root  # Keep track of the latest move node

def edit_string(sekvence, pos, jaunais_cipars):
    sekvence[pos] = jaunais_cipars
    del sekvence[pos+1]
    print(sekvence)
    

def add_alternative_moves(node, sekvence, alt_scores, player):
    """Adds two alternative future move nodes to the tree."""
    for i in range(len(sekvence) - 1):
        alt_sequence = copy.deepcopy(sekvence)
        if alt_sequence[i] == "0" and alt_sequence[i + 1] == "0":
            alt_scores[player] += 1
            alt_sequence[i] = "1"
        elif alt_sequence[i] == "0" and alt_sequence[i + 1] == "1":
            alt_scores[player] -= 1
            alt_sequence[i] = "0"
        elif alt_sequence[i] == "1" and alt_sequence[i + 1] == "0":
            alt_scores[player] -= 1
            alt_sequence[i] = "1"
        elif alt_sequence[i] == "1" and alt_sequence[i + 1] == "1":
            alt_scores[player] += 1
            alt_sequence[i] = "0"
        
        Node(f"Alt: {''.join(alt_sequence)} (P{player + 1} move) (P1: {alt_scores[0]}) (P2: {alt_scores[1]})", parent=node)


def parbaudit_izveleto(sekvence, input_pos1, input_pos2, player):
    global last_node  # Track the latest node in the tree
    if input_pos1 < 0 or input_pos2 < 0 or input_pos1 >= len(sekvence) or input_pos2 >= len(sekvence):
        return False  
    
    if not abs(input_pos1 - input_pos2) == 1 and 0 <= input_pos1 <= 25 and 0 <= input_pos2 <=25:
        return False 
    
    editing_pos = min(input_pos1, input_pos2)
    alt_scores = copy.deepcopy(scores)
    
    if sekvence[input_pos1] == "0" and sekvence[input_pos2] == "0":
        scores[player] += 1
        print("+1"), print("Player " + str(player+1) + " rezultāts: " + str(scores[player]))
        edit_string(sekvence, editing_pos, "1")
    elif sekvence[input_pos1] == "0" and sekvence[input_pos2] == "1":
        scores[player] -= 1
        print("-1"), print("Player " + str(player+1) + " rezultāts: " + str(scores[player]))
        edit_string(sekvence, editing_pos, "0")
    elif sekvence[input_pos1] == "1" and sekvence[input_pos2] == "0":
        scores[player] -= 1
        print("-1"), print("Player " + str(player+1) + " rezultāts: " + str(scores[player]))
        edit_string(sekvence, editing_pos, "1")
    elif sekvence[input_pos1] == "1" and sekvence[input_pos2] == "1":
        scores[player] += 1
        print("+1"), print("Player " + str(player+1) + " rezultāts: " + str(scores[player]))
        edit_string(sekvence, editing_pos, "0")
    else:
        return False
    
    # Add new game state as a child of the last move node
    new_node = Node(f"{''.join(sekvence)} (P{player + 1} move) (P1: {scores[0]}) (P2: {scores[1]})", parent=last_node)
    last_node = new_node  # Update the latest node pointer
    
    # Add two alternative moves to explore different play options
    add_alternative_moves(new_node, sekvence, alt_scores, player)
    
    # Print the updated decision tree
    print("\nGame Decision Tree:")
    for pre, fill, node in RenderTree(root):
        print(f"{pre}{node.name}")
    
    return True

while len(sekvence) > 1:
    try:
        if mode == "PVP":
            print()
            print()
            print("||||||||||Player " + str(player + 1) + " gājiens||||||||||")
            input_pos1 = int(input("Ievadiet pirmo pozīciju: "))
            input_pos2 = int(input("Ievadiet otro pozīciju: "))
        else:
            if player == 0:
                print()
                print()
                print("||||||||||Player " + str(player + 1) + " gājiens||||||||||")
                input_pos1 = int(input("Ievadiet pirmo pozīciju: "))
                input_pos2 = int(input("Ievadiet otro pozīciju: "))
            else:
                input_pos1, input_pos2 = 0, 1
                print()
                print()
                print("||||||||||Datora gājiens||||||||||")
                print(f"Dators izvēlējās: {input_pos1}, {input_pos2}")
        
        result = parbaudit_izveleto(sekvence, input_pos1, input_pos2, player)
        print()
        print(" \ " + str(result) + " / ")
        if player == 0 and result == True: player = 1
        else: 
            if result == True :player = 0
    except ValueError:
        print("Lūdzu ievadiet derīgus skaitļus.")

print()
print()
print()
print()
print("Apsveicu, spēle ir beigusies")
print("Player 1 rezultāts: " + str(scores[0]))
print("Player 2 rezultāts: " + str(scores[1]))
