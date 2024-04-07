import numpy as np
import torch
import connect4.game as game

_rng = np.random.default_rng(seed=1234)

_dataset = _rng.permutation(np.loadtxt('data.csv', delimiter=',', dtype=np.int8))

num_features = np.prod(np.array(game.board_shape)) # + 1 TODO: add a bit for player?
num_classes = game.board_shape[1]

_X = torch.tensor(_dataset[:,0:num_features], dtype=torch.float32)
_y = torch.tensor(_dataset[:,num_features:num_features + num_classes], dtype=torch.float32)

training_size = int(_dataset.shape[0] * 0.7)
X_train = _X[0:training_size]
y_train = _y[0:training_size]

X_test = _X[training_size:-1]
y_test = _y[training_size:-1]