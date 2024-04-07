from importlib import import_module
import random
import numpy as np
import connect4.game as game
import signal
import sys

def signal_handler(sig, frame):
    print()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

agent_x = input('enter an agent name > ').strip()
agent_y = input('enter another agent name > ').strip()
players = random.sample([
    { "name": agent_x, "agent": import_module(f"connect4.agents.{agent_x}").agent },
    { "name": agent_y, "agent": import_module(f"connect4.agents.{agent_y}").agent },
], 2)
players[0]["display"] = game.player_1
players[0]["id"] = 1
players[1]["display"] = game.player_2
players[1]["id"] = -1

state = np.zeros(game.board_shape, dtype=np.int8)
move = 0

while game.check_win(state) == 0:
    player = players[0] if move % 2 == 0 else players[1]

    # let interactive agent handle its own printing
    if player["name"] != "interactive":
        game.display_state(state)
    
    y_pred = player["agent"](state, player["display"])
    legal_pred = (state[0] == 0) * y_pred
    cols = np.flatnonzero(legal_pred == np.max(legal_pred))
    col = random.choice(cols)
    print(y_pred, cols, col)
    input("next")    
    row = np.max(np.argwhere(state[:, col] == 0))
    state[row, col] = 1 if move % 2 == 0 else -1 # TODO: use ID
    move += 1

game.display_state(state)
print(f"winner: {player['name']} ({player['display']})")
    
