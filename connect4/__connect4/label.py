import numpy as np
import random
import __connect4._game as game
import signal
import sys

def signal_handler(sig, frame):
    print()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def generate_state(num_moves: int) -> np.ndarray:
    if num_moves > 42:
        raise ValueError("can't have more than 42 moves")
    state = np.zeros(game.board_shape, dtype=np.int8)
    for i in range(num_moves):
        col = random.choice(np.nonzero(state[0] == 0)[0])
        row = np.max(np.argwhere(state[:, col] == 0))
        state[row, col] = 1 if i % 2 == 0 else -1
    return state

def encode_plan(state: np.ndarray, col: int):
    move = np.zeros(state.shape[1], dtype=np.int8)
    move[col] = 1
    return np.concatenate((np.reshape(state, -1), move), dtype=np.int8)

print("this will generate training data for the model, remember to run clean.sh after to remove duplicates and fix formatting")
with open("training.txt", "at") as out:
    while True:
        moves = random.randint(0, 41)
        state = generate_state(moves)
        possible_winner = game.check_win(state)
        if possible_winner != 0:
            continue
        game.display_state(state)

        to_play = game.player_1 if moves % 2 == 0 else game.player_2
        col = int(input("choose a column? (" + to_play + ")> ").strip())
        if col < 1 or col > state.shape[1] or state[0, col - 1] != 0:
            raise ValueError("Illegal Move")
        np.savetxt(out, encode_plan(state, col - 1), newline=",", fmt="%1d")
        print("", file=out)
        out.flush()
