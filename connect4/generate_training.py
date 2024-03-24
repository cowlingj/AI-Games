import sys
import numpy as np
import random

global board_shape
board_shape = (6, 7)
win_length = 4
player_1 = u"\x1b[91m\u25CF\x1b[0m"
player_2 = u"\x1b[93m\u25CF\x1b[0m"

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

def generate_state(num_moves: int) -> np.ndarray:
    if num_moves > 42:
        raise ValueError("can't have more than 42 moves")
    state = np.zeros(board_shape, dtype=np.int8)
    for i in range(num_moves):
        col = random.choice(np.nonzero(state[0] == 0)[0])
        row = np.max(np.argwhere(state[:, col] == 0))
        state[row, col] = 1 if i % 2 == 0 else -1
    return state

def encode_plan(state: np.ndarray, col: int):
    move = np.zeros(state.shape[1], dtype=np.int8)
    move[col] = 1
    return np.concatenate((np.reshape(state, -1), move), dtype=np.int8)


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

if __name__ == "__main__":
    print("this will generate training data for the model, remember to run clean.sh after to remove duplicates and fix formatting")
    with open("training.txt", "at") as out:
        while True:
            moves = random.randint(0, 41)
            state = generate_state(moves)
            possible_winner = check_win(state)
            if possible_winner != 0:
                continue
            display_state(state)

            to_play = player_1 if moves % 2 == 0 else player_2
            col = int(input("choose a column? (" + to_play + ")> ").strip())
            if col < 1 or col > state.shape[1] or state[0, col - 1] != 0:
                raise ValueError("Illegal Move")
            np.savetxt(out, encode_plan(state, col - 1), newline=",", fmt="%1d")
            print("", file=out)
            out.flush()
