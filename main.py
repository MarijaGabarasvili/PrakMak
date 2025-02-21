import PySimpleGUI as sg
import random

length = random.choice([15, 25])
binary_sequence = " ".join(str(random.choice([0, 1])) for _ in range(length))

layout = [[sg.Text(binary_sequence)]]
window = sg.Window("Binary Grid", layout)
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

window.close()