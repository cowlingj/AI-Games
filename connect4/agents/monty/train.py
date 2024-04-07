import torch
import torch.nn as nn
import torch.multiprocessing as mp
import torch.optim as optim
import connect4._nn_utils._dataset as dataset
from ._model import model
import numpy as np
import random
import connect4.game as game
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

def play_from_move(col: int, state: np.ndarray) -> float:
    # input("simulation")
    # game.display_state(state)
    # count illegal moves as loss
    # print(state, state.shape)
    # game.display_state(state)
    if state[0][col] != 0:
        return 0
    row = np.max(np.argwhere(state[:, col] == 0))
    state[row, col] = 1 if np.sum(state) == 0 else -1
    while game.check_win(state) == 0:
        # game.display_state(state)
        if not np.any(state[0] == 0):
            return 0.5 # draw
        cols = np.flatnonzero((state[0] == 0) * np.ones(state.shape[1]))
        rand_col = random.choice(cols)
        row = np.max(np.argwhere(state[:, rand_col] == 0))
        state[row, rand_col] = 1 if np.sum(state) == 0 else -1
    # game.display_state(state)
    return 1 - np.sum(state) # the previous player to move just won

# total simulated games = n_epocs * batch_size * simulations_per_col
def train(offset, n_epochs, my_model, loss_fn, optimizer):
    batch_size = 1000
    simulations_per_col=10

    for epoch in range(n_epochs):

        states = []
        while len(states) < batch_size:
            moves = random.randint(0, 41) # TODO: use board shape
            state = generate_state(moves)
            possible_winner = game.check_win(state)
            if possible_winner != 0:
                continue
            states.append(np.array(state))
        states = np.array(states)

        # print(states)
        torch.tensor(states.reshape((len(states), -1)), dtype=torch.float32)
        y_preds = my_model(
            torch.tensor(states.reshape((len(states), -1)), dtype=torch.float32)
        )

        ybatch = []
        for i in range(len(y_preds)):

            # legal_pred = (states[i][0] == 0) * y_preds[i].detach().numpy()
            # if np.sum(legal_pred) == 0: # agent made illegal move correct by giving list of all legal moves
            #     print("illegal move")
            #     ybatch.append(states[i][0] == 0)
            #     continue
            
            y = np.zeros(len(y_preds[i]))
            for _ in range(simulations_per_col):
                for col in range(len(y_preds[i])):
                    y[col] += play_from_move(col, np.copy(states[i]))
            # print(y_preds[i], y / simulations_per_col)
            ybatch.append(y / simulations_per_col)
        ybatch = np.array(ybatch)

        loss = loss_fn(y_preds, torch.tensor(ybatch, dtype=torch.float32))
        # print(f"Finished batch {i}, latest loss={loss}")
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(f'({offset}) Finished epoch {epoch + offset * n_epochs}, latest loss {loss}')

if __name__ == '__main__':
    # device = torch.device("cuda" if torch.cuda.is_available()  else "cpu")

    epochs_per_process = 50
    num_processes = 1
    checkpoint = input("filename: (monty.ckpt)").strip()
    if len(checkpoint) == 0:
        checkpoint = "monty.ckpt"
    
    my_model = model()
    my_model.share_memory()

    loss_fn = nn.BCELoss()
    optimizer = optim.Adam(my_model.parameters(), lr=0.01)

    processes = []
    for rank in range(num_processes):
        p = mp.Process(target=train, args=(rank, epochs_per_process, my_model, loss_fn, optimizer))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    torch.save({
            'epoch': num_processes * epochs_per_process,
            'model_state_dict': my_model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            # 'loss': loss,
    }, checkpoint)