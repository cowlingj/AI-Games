import torch
import torch.nn as nn
import torch.optim as optim
import connect4._nn_utils._dataset as dataset
from ._model import model

my_model = model()

loss_fn = nn.BCELoss()
optimizer = optim.Adam(my_model.parameters(), lr=0.0005)

n_epochs = 800
batch_size = 40

checkpoint = input("filename: (model.ckpt)").strip()
if len(checkpoint) == 0:
    checkpoint = "model.ckpt"

for epoch in range(n_epochs):
    for i in range(0, len(dataset.X_train), batch_size):
        Xbatch = dataset.X_train[i:i+batch_size]
        y_pred = my_model(Xbatch)
        ybatch = dataset.y_train[i:i+batch_size]
        loss = loss_fn(y_pred, ybatch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f'Finished epoch {epoch}, latest loss {loss}')
    torch.save({
            'epoch': epoch,
            'model_state_dict': my_model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss,
    }, checkpoint)
