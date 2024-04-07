import numpy as np
import torch
from ._model import model
import connect4._nn_utils._dataset as dataset

my_model = None

def _init():
    global my_model
    my_model = model()
    checkpoint = input("filename: (monty.ckpt)").strip()
    if len(checkpoint) == 0:
        checkpoint = "monty.ckpt"
    my_model.load_state_dict(torch.load(checkpoint)['model_state_dict'])
    my_model.eval()

def agent(state: np.ndarray, player: str) -> np.ndarray:
    global my_model
    with torch.no_grad():
        if my_model == None:
            _init()
        # print(my_model)
        return np.array(my_model(torch.tensor(state.reshape(1, -1), dtype=torch.float32)))
