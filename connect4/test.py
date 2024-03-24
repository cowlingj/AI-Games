import numpy as np
import torch
import model
import dataset

with torch.no_grad():
    nn = model.model()
    nn.load_state_dict(torch.load('model.ckpt')['model_state_dict'])
    nn.eval()
    y_pred = np.array(nn(dataset.X_test))
    rounded = np.where(y_pred == np.max(y_pred, axis=1).reshape(-1, 1), 1, 0)

    accuracy = np.all((rounded == np.array(dataset.y_test)), axis=1).mean()
    print(f"Accuracy {accuracy}")