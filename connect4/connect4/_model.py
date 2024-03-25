import torch.nn as nn
import connect4._dataset as dataset

_hidden_size = 1024
_hidden_count = 6
_layers = [ nn.Linear(dataset.num_features, _hidden_size), nn.ReLU() ] + \
    [ x for xs in [ [nn.Linear(_hidden_size, _hidden_size), nn.ReLU()] for _ in range(_hidden_count) ] for x in xs ] + \
    [ nn.Linear(_hidden_size, dataset.num_classes), nn.Sigmoid()]

model = lambda : nn.Sequential(*_layers)
