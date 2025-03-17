import PySimpleGUI as sg
import random

layout = [
    [sg.Text("", size=(16, 1)), sg.Button("Player 1"), sg.Text("", size=(33, 1)), 
    sg.Text("", size=(15, 1)), sg.Button("Player 2"), sg.Text("", size=(15, 1))],
    [sg.Text("Enter the length of the binary sequence:",
    font=("Helvetica", 20)), sg.InputText(key='-LENGTH-')],
    [sg.Text("", size=(15, 1)), sg.Button("Algorithm 1"), sg.Text("", size=(30, 1)), 
    sg.Text("", size=(15, 1)), sg.Button("Algorithm 2"), sg.Text("", size=(15, 1))],
    [sg.Text("", size=(5, 1))],
    [sg.Text(""), sg.Button("Confirm"), sg.Text("", size=(15, 1))],

    [sg.Text("", key='-OUTPUT-')]
]

window = sg.Window("Binary Sequence Generator", layout)
confirm = False
# to choose who starts the game (by default player 1)
start = 0
# to choose the algorithm (by default first algorithm)
algorithm = 0

def new_window(length):
    line = [random.choice([0, 1]) for _ in range(length)]
    button_row = [sg.Button(str(num), key=f'-BTN_{i}-') for i, num in enumerate(line)]
    new_layout = [
                [sg.Text("New Window", font=("Helvetica", 20))],
                [sg.Text(f"Generated Sequence: {line}")],
                button_row,
                [sg.Button("Close")]
            ]
    new_window = sg.Window("New Window", new_layout)
    while True:
        event, values = new_window.read()
        if event == sg.WINDOW_CLOSED or event == "Close":
            break

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
        



