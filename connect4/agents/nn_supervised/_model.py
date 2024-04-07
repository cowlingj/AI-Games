import torch.nn as nn
import connect4._nn_utils._dataset as utils

# https://datascience.stackexchange.com/questions/20222/how-to-decide-neural-network-architecture
# https://stats.stackexchange.com/questions/240305/where-should-i-place-dropout-layers-in-a-neural-network
_hidden_size = utils.num_features
_hidden_count = 50
_layers = [ nn.Linear(utils.num_features, _hidden_size), nn.ReLU() ] + \
    [ x for xs in [ [nn.Linear(_hidden_size, _hidden_size), nn.ReLU(), nn.Dropout() ] for _ in range(_hidden_count) ] for x in xs ] + \
    [ nn.Linear(_hidden_size, utils.num_classes), nn.Sigmoid() ]

model = lambda : nn.Sequential(*_layers)
