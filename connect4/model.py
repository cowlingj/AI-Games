import numpy as np
import numpy as np
import torch.nn as nn
import torch.optim as optim

board_shape = (6, 7)

_hidden_size = 1024
_hidden_count = 6
_layers = [ nn.Linear(np.prod(np.array(board_shape)), _hidden_size), nn.ReLU() ] + \
    [ x for xs in [ [nn.Linear(_hidden_size, _hidden_size), nn.ReLU()] for _ in range(_hidden_count) ] for x in xs ] + \
    [ nn.Linear(_hidden_size, board_shape[1]), nn.Sigmoid()]

model = lambda : nn.Sequential(*_layers)
