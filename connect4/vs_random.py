import sys
import time
import numpy as np
import random
import sys
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

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

hidden_size = 1024
hidden_count = 6
layers = [ nn.Linear(np.prod(np.array(board_shape)), hidden_size), nn.ReLU() ] + \
    [ x for xs in [ [nn.Linear(hidden_size, hidden_size), nn.ReLU()] for _ in range(hidden_count) ] for x in xs ] + \
    [ nn.Linear(hidden_size, board_shape[1]), nn.Sigmoid()]

model = nn.Sequential(
    *layers
)

if __name__ == "__main__":
    model.load_state_dict(torch.load('model.pkl'))
    games = 0
    wins = 0
    while True:
        state = np.zeros(board_shape, dtype=np.int8)
        move = 0
        starting = random.choice(("NN", "R"))
        with torch.no_grad():
            while check_win(state) == 0:
                if not np.any(state[0] == 0):
                    print("draw")
                    player = None
                # print(state)
                to_play = player_1 if move % 2 == 0 else player_2
                player = "NN" if (starting == "NN" and to_play == player_1) or (starting == "R" and to_play == player_2) else "R"

                display_state(state)
                print(f"{player} to play")
                # print(torch.tensor(state.reshape(1, -1), dtype=torch.float32))

                if player == "R":
                    col = random.choice(np.nonzero(state[0] == 0)[0])
                    print(f"R wants to play {col + 1}")
                    row = np.max(np.argwhere(state[:, col] == 0))
                    state[row, col] = 1 if move % 2 == 0 else -1
                else:
                    y_pred = np.array(model(torch.tensor(state.reshape(1, -1), dtype=torch.float32)))

                    print((state[0] == 0), ((state[0] == 0) * y_pred)[0])
                    col = np.argmax((state[0] == 0) * y_pred)
                    if np.sum((state[0] == 0) * y_pred) == 0:
                        print("NN doesn't have any suggestions, picking at random")
                        col = random.choice(np.nonzero(state[0] == 0)[0])
                    print(f"NN wants to play {col + 1}")
                    if col < 0 or col >= state.shape[1] or state[0, col] != 0:
                        raise ValueError("Illegal Move")
                    row = np.max(np.argwhere(state[:, col] == 0))
                    state[row, col] = 1 if move % 2 == 0 else -1
                move += 1
            if player == None: # don't count draws either way
                break
            if player == "NN":
                wins += 1
            games += 1
            print(f"winner: {player} - games: {games}, wins: {wins} ({100 * wins/games}%)")
            time.sleep(0.1)
        
