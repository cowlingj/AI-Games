import os
import time
import numpy as np
import random
import torch
import __connect4._game as game
import __connect4._model as model
import signal
import sys

def signal_handler(sig, frame):
    print()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

my_model = model.model()

my_model.load_state_dict(torch.load('model.ckpt')['model_state_dict'])
my_model.eval()
games = 0
wins = 0
losses = 0
draws = 0

debug = os.environ.get('DEBUG', "False").lower() == "true"
def debug_print(*args, **kwargs) -> None:
    if debug:
        print(*args, **kwargs)

print("simulating games against an opponent playing randomly")

while True:
    state = np.zeros(game.board_shape, dtype=np.int8)
    move = 0
    starting = random.choice(("NN", "R"))
    with torch.no_grad():
        while game.check_win(state) == 0:
            if not np.any(state[0] == 0):
                player = None
                break
            to_play = game.player_1 if move % 2 == 0 else game.player_2
            player = "NN" if (starting == "NN" and to_play == game.player_1) or (starting == "R" and to_play == game.player_2) else "R"

            if debug:
                game.display_state(state)
            debug_print(f"{player} to play")

            if player == "R":
                col = random.choice(np.nonzero(state[0] == 0)[0])
                debug_print(f"R wants to play {col + 1}")
                row = np.max(np.argwhere(state[:, col] == 0))
                state[row, col] = 1 if move % 2 == 0 else -1
            else:
                y_pred = np.array(my_model(torch.tensor(state.reshape(1, -1), dtype=torch.float32)))
                debug_print(y_pred)
                legal_pred = (state[0] == 0) * y_pred
                cols = np.nonzero(legal_pred == np.max(legal_pred))
                col = random.choice(cols)
                debug_print(f"NN wants to play {col + 1}")
                if col < 0 or col >= state.shape[1] or state[0, col] != 0:
                    raise ValueError("Illegal Move")
                row = np.max(np.argwhere(state[:, col] == 0))
                state[row, col] = 1 if move % 2 == 0 else -1
            move += 1
        games += 1
        if player == None: # don't count draws
            draws += 1
            debug_print("draw")
        elif player == "NN":
            wins += 1
            debug_print("NN wins")
        else:
            losses +=1
            debug_print("NN loses")
        
        if debug:
            print(f"win rate: {100 * wins/games:06.2f}% games: {games:08d}, (W/L/D) ({wins:08d}/{losses:08d}/{draws:08d})")
            time.sleep(0.1)
        else:
            print(f"\rwin rate: {100 * wins/games:06.2f}% games: {games:08d}, (W/L/D) ({wins:08d}/{losses:08d}/{draws:08d})", end="")