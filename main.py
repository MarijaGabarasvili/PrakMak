import PySimpleGUI as sg
import random
import game_tree as gt
import computer_player as algo

layout = [
    [sg.Text("Choose player or computer:", font=("Helvetica", 16))],
    [sg.Text("1st turn:", font=("Helvetica", 14))],
    [sg.Radio("Player", "1PLAYER_GROUP", key="-PLAYER1-", font=("Helvetica", 14)), 
     sg.Radio("Computer", "1PLAYER_GROUP", key="-COMPUTER1-", font=("Helvetica", 14))],
    [sg.Text("2nd turn:", font=("Helvetica", 14))],
    [sg.Radio("Player", "2PLAYER_GROUP", key="-PLAYER2-", font=("Helvetica", 14)), 
     sg.Radio("Computer", "2PLAYER_GROUP", key="-COMPUTER2-", font=("Helvetica", 14))],
    [sg.Text("Enter the length of the binary sequence:", font=("Helvetica", 16)), sg.InputText(key='-LENGTH-')],
    [sg.Text("Choose Algorithm:", font=("Helvetica", 16)), sg.Button("Minmax"), sg.Text("", size=(5, 1)), sg.Button("Alfa-beta"), sg.Text("", size=(15, 1))],
    [sg.Text("")],
    [sg.Text(""), sg.Button("Confirm"), sg.Text("", size=(15, 1))],
    [sg.Text("", key='-OUTPUT-')]
]

window = sg.Window("Binary Sequence Generator", layout)
confirm = False
algorithm = 0
is_computer_1 = False
is_computer_2 = False

def rules(pressed):
    global points
    points = 0
    number = 0 
    if pressed[0] == 0 and pressed[1] == 0:
        points += 1
        number = 1
    elif pressed[0] == 0 and pressed[1] == 1:
        points -= 1
        number = 0
    elif pressed[0] == 1 and pressed[1] == 0:
        points -= 1
        number = 1
    elif pressed[0] == 1 and pressed[1] == 1:
        points += 1
        number = 0
    return number

def detect_merge_indices(prev_seq: str, next_seq: str):
    for i in range(len(prev_seq) - 1):
        pair = (prev_seq[i], prev_seq[i + 1])
        if pair == ('0', '0'):
            merged = '1'
        elif pair == ('0', '1'):
            merged = '0'
        elif pair == ('1', '0'):
            merged = '1'
        elif pair == ('1', '1'):
            merged = '0'
        test_seq = prev_seq[:i] + merged + prev_seq[i + 2:]
        if test_seq == next_seq:
            return i, i + 1
    return None

def new_window(length):
    line = [random.choice([0, 1]) for _ in range(length)]
    button_row = [sg.Button(str(num), key=f'-BTN_{i}-') for i, num in enumerate(line)]
    current_player = 0
    player1_points = 0
    player2_points = 0
    end_game_flag = False

    cmp1 = algo.ComputerPlayer("minimax" if algorithm == 0 else "alpha_beta") if is_computer_1 else None
    cmp2 = algo.ComputerPlayer("minimax" if algorithm == 0 else "alpha_beta") if is_computer_2 else None

    layout_game = [
        [sg.Text("Score:", font=("Helvetica", 20))],
        [sg.Text("Player 1 Points:", font=("Helvetica", 14)), sg.Text(f"{player1_points}", key='-P1_POINTS-', size=(5, 1)),
         sg.Text("Player 2 Points:", font=("Helvetica", 14)), sg.Text(f"{player2_points}", key='-P2_POINTS-', size=(5, 1))],
        [sg.Text(f"Generated Sequence: {line}", key='-SEQUENCE-')],
        button_row,
        [sg.Text(f"Current Turn: Player {current_player + 1}", key='-TURN-', font=("Helvetica", 14))],
        [sg.Button("Close")]
    ]

    window_game = sg.Window("New Window", layout_game, finalize=True)
    pressed_butt = []

    while True:
        if len(line) == 1 and not end_game_flag:
            if player1_points > player2_points:
                winner_text = f"Player 1 wins with {player1_points} points!"
            elif player2_points > player1_points:
                winner_text = f"Player 2 wins with {player2_points} points!"
            else:
                winner_text = "It's a tie!"

            if cmp1 or cmp2:
                cpu_nodes = 0
                if cmp1:
                    cpu_nodes += cmp1.nodes_visited
                if cmp2:
                    cpu_nodes += cmp2.nodes_visited

                print(f"CPU visited {cpu_nodes} nodes.")
                node_info = f"\nCPU visited {cpu_nodes} nodes."
                window_game['-SEQUENCE-'].update(winner_text + node_info)
            else:
                window_game['-SEQUENCE-'].update(winner_text)

            end_game_flag = True

        if end_game_flag:
            event, _ = window_game.read()
            if event == sg.WINDOW_CLOSED or event == "Close":
                window_game.close()
                break
            continue

        is_cpu = ((current_player == 0 and is_computer_1) or (current_player == 1 and is_computer_2))
        if is_cpu:
            cmp = cmp1 if current_player == 0 else cmp2
            game_tree = gt.GameTree("".join(map(str, line)), depth_limit=10)
            path, _ = cmp.get_path(game_tree.root, is_maximizing=(current_player == 0))

            if len(path) >= 2:
                merge_indices = detect_merge_indices(path[0].sequence, path[1].sequence)
                if merge_indices:
                    pressed_butt = list(merge_indices)
        else:
            event, values = window_game.read()
            if event == sg.WINDOW_CLOSED or event == "Close":
                window_game.close()
                break

            if event.startswith('-BTN_'):
                index = int(event.split('_')[1].split('-')[0])
                if len(pressed_butt) < 2 and (not pressed_butt or abs(pressed_butt[-1] - index) == 1):
                    pressed_butt.append(index)
                    for i in range(len(line)):
                        if len(pressed_butt) == 1 and abs(index - i) == 1:
                            window_game[f'-BTN_{i}-'].update(disabled=False)
                        else:
                            window_game[f'-BTN_{i}-'].update(disabled=True)
                    window_game[event].update(disabled=True)

        if len(pressed_butt) == 2:
            selected_numbers = [line[pressed_butt[0]], line[pressed_butt[1]]]
            number = rules(selected_numbers)

            if current_player == 0:
                player1_points += points
            else:
                player2_points += points

            window_game['-P1_POINTS-'].update(player1_points)
            window_game['-P2_POINTS-'].update(player2_points)

            first_index = pressed_butt[0]
            second_index = pressed_butt[1]
            line[first_index] = number
            del line[second_index]

            window_game['-SEQUENCE-'].update(f"Generated Sequence: {line}")
            for i in range(len(line)):
                window_game[f'-BTN_{i}-'].update(str(line[i]), disabled=False, visible=True)
            for i in range(len(line), length):
                window_game[f'-BTN_{i}-'].update(visible=False)

            current_player = 1 - current_player
            window_game['-TURN-'].update(f"Current Turn: Player {current_player + 1}")
            pressed_butt = []

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    try:
        length = int(values['-LENGTH-'])
        confirm = 1 < length < 26
    except ValueError:
        window['-OUTPUT-'].update("Please enter a number between 15 and 25.")

    if values["-COMPUTER1-"]:
        is_computer_1 = True
    if values["-COMPUTER2-"]:
        is_computer_2 = True

    if event == "Minmax":
        algorithm = 0
    elif event == "Alfa-beta":
        algorithm = 1

    if event == "Confirm" and confirm:
        window.close()
        new_window(length)

window.close()
        