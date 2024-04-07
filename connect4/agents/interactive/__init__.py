

import numpy as np

from connect4 import game

def agent(state: np.ndarray, player: str) -> np.ndarray:
    game.display_state(state)
    col = int(input("choose a column? (" + player + ")> ").strip())
    if col < 1 or col > state.shape[1] or state[0, col - 1] != 0:
        raise ValueError("Illegal Move")
    cols = np.zeros(state.shape[1], dtype=bool)
    cols[col - 1] = True
    return cols