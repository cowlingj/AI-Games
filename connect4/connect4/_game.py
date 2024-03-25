import os
import numpy as np

board_shape = (6, 7)
win_length = 4
# default players are red/yellow circles by default
player_1 = u"\x1b[91m\u25CF\x1b[0m" if os.environ.get("COLOR", "true") != "false" else "X"
player_2 = u"\x1b[93m\u25CF\x1b[0m" if os.environ.get("COLOR", "true") != "false" else "O"

def display_state(state: np.ndarray):
    print(" 1  2  3  4  5  6  7")
    for col in state:
        for cell in col:
            if cell == 0:
                print("| |", end="")
            elif cell == 1:
                print("|" + player_1 + "|", end="")
            elif cell == -1:
                print("|" + player_2 + "|", end="")
            else:
                raise ValueError("state should be ndarray(6, 7) of 0, 1, or -1")
        print("")

def check_win(state: np.ndarray) -> int:
    for direction in (
        state,
        state.T,
        [state.diagonal(i) for i in range(state.shape[1]-1,-state.shape[0],-1)],
        [np.fliplr(state).diagonal(i) for i in range(state.shape[1]-1,-state.shape[0],-1)]
    ):
        for col in direction:
            in_a_row = 0
            player = 0
            for cell in col:
                if cell == 0:
                    in_a_row = 0
                    player = 0
                    continue

                if cell != player:
                    in_a_row = 1
                    player = cell
                    continue
                
                in_a_row += 1
                if in_a_row >= win_length:
                    return player
    return 0