import PySimpleGUI as sg
from computer_player import ComputerPlayer
from game_tree import GameTree
import time

str_blue = "\033[34m"
str_red = "\033[31m"
str_green = "\033[32m"
str_yellow = "\033[33m"
str_reset = "\033[0m"

default_depth_limit = 5

class GameGUI:
    player1_type : str
    player2_type : str
    intial_sequence_len : int
    _button_keys : list
    _default_btn_clr : str
    _highlight_btn_clr : str
    _player_types = {
                        'Human': 'human',
                        'PC (Minimax)': 'minimax',
                        'PC (Alpha-Beta)': 'alpha_beta',
                        'PC (Greedy)': 'heuristic'
                    }
    _default_sequence_length : int = 10
    
    def __init__(self):
        sg.theme('DarkGrey11')
        default_btn_fg, default_btn_bg = sg.theme_button_color()
        self._default_btn_clr = (default_btn_fg, default_btn_bg)
        self._highlight_btn_clr = (default_btn_bg, default_btn_fg)
        self.set_settings_dialog()

    def set_settings_dialog(self):
        layout = [
            [sg.Text("Player 1:"), sg.Push(), sg.Combo(list(self._player_types.keys()), default_value='Human', key='P1', size=(18, 1))],
            [sg.Column([[]], size=(1, 1), pad=(2, 2))],
            [sg.Text("Player 2:"), sg.Push(), sg.Combo(list(self._player_types.keys()), default_value='PC (Minimax)', key='P2', size=(18, 1))],
            [sg.Column([[]], size=(1, 1), pad=(2, 2))],
            [sg.Text("Length of sequence (1-25):"), sg.Push(), sg.InputText(default_text=f'{self._default_sequence_length}', key='SEQ', size=(5, 1))],
            [sg.Text('', pad=(0, (1, 1)))],
            [sg.Push(), sg.Button("Start", size=(10,1)), sg.Push()]
        ]
        window = sg.Window("Settings", layout)
        
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                window.close()
                exit()

            if event == "Start":
                try:
                    seq_length = int(values['SEQ'])
                    if 1 <= seq_length <= 25:
                        break
                    else:
                        sg.popup_error("Length must be between 1 and 25!")
                        window['SEQ'].update(f'{self.default_sequence_length}')
                        
                except ValueError:
                    sg.popup_error("Please enter a valid number for sequence length.")
                    window['SEQ'].update(f'{self.default_sequence_length}')

        window.close()
        
        self.player1_type = self._player_types.get(values['P1'], None)
        self.player2_type = self._player_types.get(values['P2'], None)
        self.intial_sequence_len = int(values['SEQ'])

    def open_game_dialog(self, game_sequence):
        self._button_keys = [f"BTN_{i}" for i in range(self.intial_sequence_len)]
        layout = [
                [sg.Text("Player 1:", pad=(0, 0)), sg.Text('0', key='text_score_p1', size=(3, 1), justification='left', pad=(0, 0)),
                sg.Push(), sg.Text("Click two adjacent buttons to remove them"),sg.Push(),
                sg.Text("Player 2:", pad=(0, 0)), sg.Text('0', key='text_score_p2', size=(3, 1), justification='left', pad=(0, 0))],
                [sg.Push(), *[sg.Button(char, key=key, size=(2, 1), pad=(0, 0), font=("Helvetica", 10)) for char, key in zip(game_sequence, self._button_keys)], sg.Push()]
            ]
        self._play_game_window = sg.Window("Match buttons", layout, size=(550, 100), finalize=True)

    def game_finished(self, str_player_won):
        layout = [
            [sg.Push(), sg.Text(str_player_won, font=("Helvetica", 14)), sg.Push()],
            [sg.Column([[]], size=(1, 1), pad=(2, 2))],
            [sg.Push(), sg.Button("Exit", size=(10,1)), sg.Push(), sg.Button("Restart", size=(10,1)), sg.Push()]
        ]
        self._play_game_window.close()
        window = sg.Window("Game Over", layout)
        
        while True:
            event, _ = window.read()
            if event == sg.WINDOW_CLOSED or event == "Exit":
                window.close()
                exit()
            elif event == "Restart":
                window.close()
                break

    def get_user_move(self):
        """
        Wait for the user to click two adjacent buttons.
        Returns the index (extracted from the button key) of the left-most button in the selected pair.
        This version assumes that the current sequence is fully represented by the buttons,
        and that update_sequence() rebuilds the button row if the sequence changes.
        """
        selected_index = None
        while True:
            event, _ = self._play_game_window.read()
            
            if event in (sg.WINDOW_CLOSED, None):
                self._play_game_window.close()
                exit()  # or raise an exception / return None depending on how you want to handle it
            
            if event is None:
                continue
            # Only process events coming from buttons with keys starting with "BTN_"
            if event.startswith("BTN_"):
                current_index = int(event.split("_")[1])
                if selected_index is None:
                    # First selection: highlight it.
                    selected_index = current_index
                    self._play_game_window[event].update(button_color=self._highlight_btn_clr)
                else:
                    # Check if the two indices are adjacent based on the current sequence order.
                    if abs(current_index - selected_index) == 1:
                        # Determine the left-most index.
                        left_index = min(selected_index, current_index)
                        # Optionally, reset the button colors
                        self._play_game_window[f"BTN_{selected_index}"].update(button_color=self._default_btn_clr)
                        self._play_game_window[event].update(button_color=(None, None))
                        return left_index
                    else:
                        # If not adjacent, reset previous selection and start new.
                        self._play_game_window[f"BTN_{selected_index}"].update(button_color=self._default_btn_clr)
                        selected_index = current_index
                        self._play_game_window[event].update(button_color=self._highlight_btn_clr)
            # Ignore other events 
    
    def update_sequence(self, sequence: str):
        for i, key in enumerate(self._button_keys):
            if i < len(sequence):
                self._play_game_window[key].update(text=sequence[i], visible=True)
            else:
                self._play_game_window[key].update(visible=False)

    def update_score(self, score_player1, score_player2):
        """
        Update the score texts on the GUI.
        """
        self._play_game_window['text_score_p1'].update(score_player1)
        self._play_game_window['text_score_p2'].update(score_player2)

gui = GameGUI()

while True:
    print(f"{str_blue}Starting game: {gui.player1_type} vs {gui.player2_type}, Sequence Length: {gui.intial_sequence_len}{str_reset}")

    print(f"{str_blue}Generating game tree... ", end="")
    timer = time.time()
    game_tree = GameTree(gui.intial_sequence_len, default_depth_limit)
    timer = time.time() - timer
    print(f"done in {timer:.6f} seconds, starting sequence {game_tree.initial_sequence}, depth limit {game_tree.depth_limit}\n{str_reset}")
    gui.open_game_dialog(game_tree.initial_sequence)

    predicted_score = None
    if gui.player1_type != 'human':
        pc_player1 = ComputerPlayer(gui.player1_type)
        path, predicted_score = pc_player1.get_path(game_tree.current_state, True)
    else:
        pc_player1 = None
        
    if gui.player2_type != 'human':
        pc_player2 = ComputerPlayer(gui.player2_type)
        path, predicted_score = pc_player2.get_path(game_tree.current_state, True)
    else:
        pc_player2 = None

    print(f"{str_blue}Game started. {str_reset}", end="")
    if predicted_score != None:
        if predicted_score > 0:
            print(f"{str_red}Player 1 predicted to win.\n{str_reset}")
        elif predicted_score < 0:
            print(f"{str_green}Player 2 predicted to win.\n{str_reset}")
        else:
            print(f"{str_yellow}The game is predicted to end in a draw.\n{str_reset}")
    else:
        print("\n")

    while game_tree.current_state.children:
        is_player1 = game_tree.get_current_player() == 1
        player_type = gui.player1_type if is_player1 else gui.player2_type
        pc_player = pc_player1 if is_player1 else pc_player2
        player_label = "Player 1" if is_player1 else "Player 2"
        color = str_red if is_player1 else str_green

        print(f"{color}Move #{game_tree.current_depth} - {game_tree.current_state} {player_label} move:", end="")

        if player_type == 'human':
            first_digit_to_join = gui.get_user_move()
            game_tree.move_to_next_state_by_move(first_digit_to_join)
        else:
            optimal_path, _ = pc_player.get_path(game_tree.current_state, is_player1)
            game_tree.move_to_next_state_by_child(optimal_path[1])

        print(f"{game_tree.current_state}{str_reset}")
        gui.update_sequence(game_tree.current_state.sequence)
        gui.update_score(game_tree.current_state.score_player1, game_tree.current_state.score_player2)

    if game_tree.current_state.score_player1 > game_tree.current_state.score_player2:
        str_player_won = "Player 1 wins!"
    elif game_tree.current_state.score_player1 < game_tree.current_state.score_player2:
        str_player_won = "Player 2 wins!"
    else:
        str_player_won = "It's a draw!"
            
    print(f"{str_blue}Game over. {str_player_won}{str_reset}")
    if pc_player1 != None:
        print(f"{str_blue}Game tree nodes visited by Player 1 ({pc_player1.algorithm}): {pc_player1.nodes_visited}{str_reset}")
    if pc_player2 != None:
        print(f"{str_blue}Game tree nodes visited by Player 2 ({pc_player2.algorithm}): {pc_player2.nodes_visited}{str_reset}")
        
    gui.game_finished(str_player_won)
    gui.set_settings_dialog()