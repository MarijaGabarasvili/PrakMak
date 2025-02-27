import PySimpleGUI as sg
import random

layout = [
    [sg.Text("", size=(16, 1)), sg.Button("Player 1"), sg.Text("", size=(33, 1)), sg.Text("", size=(15, 1)), sg.Button("Player 2"), sg.Text("", size=(15, 1))],
    [sg.Text("Enter the length of the binary sequence:",font=("Helvetica", 20)), sg.InputText(key='-LENGTH-')],
    [sg.Text("", size=(40, 1)), sg.Button("Generate", size=(20, 2))],
    [sg.Text("", size=(15, 1)), sg.Button("Algorithm 1"), sg.Text("", size=(30, 1)), sg.Text("", size=(15, 1)), sg.Button("Algorithm 2"), sg.Text("", size=(15, 1))],

    [sg.Text("", key='-OUTPUT-')]
]

window = sg.Window("Binary Sequence Generator", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == "Generate":
        try:
            length = int(values['-LENGTH-'])
            if length <= 14 or length >= 26:
                window['-OUTPUT-'].update("Please enter a number between 15 and 25.")
                continue
            line = " ".join(str(random.choice([0, 1])) for _ in range(length))
            window['-OUTPUT-'].update(line)
        except ValueError:
            window['-OUTPUT-'].update("Please enter a number between 15 and 25.")

window.close()