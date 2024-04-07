import numpy as np
import torch
from ._model import model
import connect4._nn_utils._dataset as dataset

with torch.no_grad():
    my_model = model()
    my_model.load_state_dict(torch.load('model.ckpt')['model_state_dict'])
    my_model.eval()
    y_pred = np.array(my_model(dataset.X_test))
    rounded = np.where(y_pred == np.max(y_pred, axis=1).reshape(-1, 1), 1, 0)

    accuracy = np.all((rounded == np.array(dataset.y_test)), axis=1).mean()
    print(f"Accuracy {accuracy}")