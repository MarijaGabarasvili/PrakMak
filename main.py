# Should include GUI and the main logic of the program
import PySimpleGUI as sg
import random


layout = [
    [sg.Text("Choose Player:", font=("Helvetica", 16)), sg.Button("Player 1"), sg.Text("", size=(5, 1)), 
    sg.Text("", size=(15, 1)), sg.Button("Player 2"), sg.Text("", size=(15, 1))],
    [sg.Text("Enter the length of the binary sequence:",
    font=("Helvetica", 16)), sg.InputText(key='-LENGTH-')],
    [sg.Text("Choose Algorithm:", font=("Helvetica", 16)),
     sg.Button("Algorithm 1"), sg.Text("", size=(5, 1)), sg.Button("Algorithm 2"), sg.Text("", size=(15, 1))],
    [sg.Text("")],
    [sg.Text(""), sg.Button("Confirm"), sg.Text("", size=(15, 1))],

    [sg.Text("", key='-OUTPUT-')]
]

window = sg.Window("Binary Sequence Generator", layout)
confirm = False
# to choose who starts the game (by default player 1)
start = 0
# to choose the algorithm (by default first algorithm)
algorithm = 0
points = 0 #score

# take from game tree file
def rules(pressed):
    global points
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
    line = [random.choice([0, 1]) for _ in range(length)] #take to the game tree file
    button_row = [sg.Button(str(num), key=f'-BTN_{i}-') for i, num in enumerate(line)]
    current_player = start
    
    new_layout = [
        [sg.Text("New Window", font=("Helvetica", 20))],
        [sg.Text(f"Generated Sequence: {line}", key='-SEQUENCE-')],
        button_row,
        [sg.Text(f"Current Turn: Player {current_player}", key='-TURN-', font=("Helvetica", 14))],
        [sg.Button("Close")]
    ]
    
    new_window = sg.Window("New Window", new_layout)
    
    
    while len(line) > 1:
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
            if len(pressed_butt) == 2:
                
                selected_numbers = [line[pressed_butt[0]], line[pressed_butt[1]]]
                number = rules(selected_numbers)
                
                first_index = pressed_butt[0]
                second_index = pressed_butt[1]
                line[first_index] = number
                del line[second_index]
                
                new_window['-SEQUENCE-'].update(f"Generated Sequence: {line}")
                for i in range(len(line)):
                    new_window[f'-BTN_{i}-'].update(str(line[i]), disabled=False, visible=True)
                for i in range(len(line), length):
                    new_window[f'-BTN_{i}-'].update(visible=False)
                    
                current_player = 1 if current_player == 2 else 2
                new_window['-TURN-'].update(f"Current Turn: Player {current_player}")
                pressed_butt = []
                
    if len(line) == 1:
        new_window['-TURN-'].update(f"Player {current_player} wins!")
    
           
    

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
    if event == "Player 1":
        start = 1
    if event == "Player 2":
        start = 2
    if event == "Algorithm 1":
        algorithm = 1
    if event == "Algorithm 2":
        algorithm = 2
    if start == 0:
        window['-OUTPUT-'].update("Please select a player to start.")
    if algorithm == 0:  
        window['-OUTPUT-'].update("Please select an algorithm.")
    if event == "Confirm":
        if confirm and start != 0 and algorithm != 0:
            window.close()
            new_window(length)

window.close()
        