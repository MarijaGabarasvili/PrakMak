# Should include GUI and the main logic of the program
# Should include GUI and the main logic of the program
import PySimpleGUI as sg
import random
import game_tree as gt
import minimax as mm


layout = [
    [sg.Text("Choose player or computer:", font=("Helvetica", 16))],
    [sg.Text("1st turn:", font=("Helvetica", 14))],
    [sg.Radio("Player", "1PLAYER_GROUP", key="-PLAYER1-", font=("Helvetica", 14)), 
     sg.Radio("Computer", "1PLAYER_GROUP", key="-COMPUTER1-", font=("Helvetica", 14))],
    [sg.Text("2nd turn:", font=("Helvetica", 14))],
    [sg.Radio("Player", "2PLAYER_GROUP", key="-PLAYER2-", font=("Helvetica", 14)), 
     sg.Radio("Computer", "2PLAYER_GROUP", key="-COMPUTER2-", font=("Helvetica", 14))],
    [sg.Text("Enter the length of the binary sequence:",
    font=("Helvetica", 16)), sg.InputText(key='-LENGTH-')],
    [sg.Text("Choose Algorithm:", font=("Helvetica", 16)),
     sg.Button("Minmax"), sg.Text("", size=(5, 1)), sg.Button("Alfa-beta"), sg.Text("", size=(15, 1))],
    [sg.Text("")],
    [sg.Text(""), sg.Button("Confirm"), sg.Text("", size=(15, 1))],

    [sg.Text("", key='-OUTPUT-')]
]

window = sg.Window("Binary Sequence Generator", layout)
confirm = False

# to choose the algorithm (by default minmax algorithm)
algorithm = 0
is_computer_1 = False # to check if the player 1 is a computer or not (by default False)
is_computer_2 = False # to check if the player 1 is a computer or not (by default False)


# take from game tree file
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

    


def new_window(length):
    line = [random.choice([0, 1]) for _ in range(length)] #take to the game tree filew
    button_row = [sg.Button(str(num), key=f'-BTN_{i}-') for i, num in enumerate(line)]
    current_player = 0 #always starts from 1st player
    player1_points = 0 # score of player 1
    player2_points = 0 # score of player 2
    
    new_layout = [
        [sg.Text("Score:", font=("Helvetica", 20))],
        [sg.Text("Player 1 Points:", font=("Helvetica", 14)), sg.Text(f"{player1_points}", key='-P1_POINTS-', size=(5, 1)),
         sg.Text("Player 2 Points:", font=("Helvetica", 14)), sg.Text(f"{player2_points}", key='-P2_POINTS-', size=(5, 1))],
        [sg.Text(f"Generated Sequence: {line}", key='-SEQUENCE-')],
        button_row,
        [sg.Text(f"Current Turn: Player {current_player + 1}", key='-TURN-', font=("Helvetica", 14))],
        [sg.Button("Close")]
    ]
    
    new_window = sg.Window("New Window", new_layout)
    pressed_butt = []
    
    while True:
        if is_computer_1 or is_computer_2:
            if algorithm == 0:
                # Minmax algorithm
                # Implement the Minmax algorithm here
                pass
            else:
                # Alfa-beta algorithm
                # Implement the Alfa-beta algorithm here
                pass
        else:
            #maybe make a function for this
            event, values = new_window.read()
        
            if event == sg.WINDOW_CLOSED or event == "Close":
                break

            if event.startswith('-BTN_'):
                index = int(event.split('_')[1].split('-')[0])

                if len(pressed_butt) < 2 and (not pressed_butt or abs(pressed_butt[-1] - index) == 1):
                    pressed_butt.append(index)
                    for i in range(len(line)):
                        if len(pressed_butt) == 1 and abs(index - i) == 1:
                            new_window[f'-BTN_{i}-'].update(disabled=False)
                        else:
                            new_window[f'-BTN_{i}-'].update(disabled=True)
                    new_window[event].update(disabled=True)

            #maybe make a function for this
            if len(pressed_butt) == 2:
                selected_numbers = [line[pressed_butt[0]], line[pressed_butt[1]]]
                number = rules(selected_numbers)

                #add poiints
                if current_player == 0:
                    player1_points += points
                else:
                    player2_points += points

                #update points in the window
                new_window['-P1_POINTS-'].update(player1_points)
                new_window['-P2_POINTS-'].update(player2_points)
                
                first_index = pressed_butt[0]
                second_index = pressed_butt[1]
                line[first_index] = number
                del line[second_index]
                
                new_window['-SEQUENCE-'].update(f"Generated Sequence: {line}")
                for i in range(len(line)):
                    new_window[f'-BTN_{i}-'].update(str(line[i]), disabled=False, visible=True)
                for i in range(len(line), length):
                    new_window[f'-BTN_{i}-'].update(visible=False)
                    
                if current_player == 0:
                    current_player = 1
                    new_window['-TURN-'].update(f"Current Turn: {current_player + 1}")
                else:
                    current_player = 0
                    new_window['-TURN-'].update(f"Current Turn: {current_player + 1}")
                pressed_butt = []

            if len(line) == 1:     
                if player1_points>player2_points:
                    new_window['-SEQUENCE-'].update(f"Player 1 wins with {player1_points} points!")
                elif player2_points>player1_points:
                    new_window['-SEQUENCE-'].update(f"Player 2 wins with {player2_points} points!")
                else:
                    new_window['-SEQUENCE-'].update(f"It's a tie!")
        
    
           
    

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    try:
        length = int(values['-LENGTH-'])
        if length <= 14 or length >= 26:
            confirm = False
        else:
            confirm = True
    except ValueError:
            window['-OUTPUT-'].update("Please enter a number between 15 and 25.")

    # choose player
    if values["-COMPUTER1-"] == True:
        is_computer_1 = True
    if values["-COMPUTER2-"] == True:
        is_computer_2= True

    #choose algorithm   
    match event:
        case "Minmax":
            algorithm = 0
        case "Alfa-beta":
            algorithm = 1


    if event == "Confirm":
        if confirm:
            window.close()
            new_window(length)

window.close()
        