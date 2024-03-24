import numpy as np
import torch

_rng = np.random.default_rng()

_dataset = _rng.permutation(np.loadtxt('data.csv', delimiter=',', dtype=np.int8))

_X = torch.tensor(_dataset[:,0:42], dtype=torch.float32)
_y = torch.tensor(_dataset[:,42:49], dtype=torch.float32)

training_size = 400
X_train = _X[0:training_size]
y_train = _y[0:training_size]

X_test = _X[training_size:-1]
y_test = _y[training_size:-1]