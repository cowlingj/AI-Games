import numpy as np
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
state = np.zeros(game.board_shape, dtype=np.int8)
move = 0
with torch.no_grad():
    while game.check_win(state) == 0:
        game.display_state(state)
        to_play = game.player_1 if move % 2 == 0 else game.player_2
        print("suggestions")
        y_pred = np.array2string(
            np.array(my_model(torch.tensor(state.reshape(1, -1), dtype=torch.float32))),
            precision=0,
            separator=', ',
            suppress_small=True,
            formatter={"all": lambda x: str(int(100 * x))}
        )
        print(y_pred)
        col = int(input("choose a column? (" + to_play + ")> ").strip())
        if col < 1 or col > state.shape[1] or state[0, col - 1] != 0:
            raise ValueError("Illegal Move")
        row = np.max(np.argwhere(state[:, col - 1] == 0))
        state[row, col - 1] = 1 if move % 2 == 0 else -1
        move += 1
    print(f"winner: {to_play}")
    
