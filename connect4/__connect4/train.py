import torch
import torch.nn as nn
import torch.optim as optim
import __connect4._dataset as dataset
import __connect4._model as model

my_model = model.model()

loss_fn = nn.BCELoss()
optimizer = optim.Adam(my_model.parameters(), lr=0.0006)

n_epochs = 100
batch_size = 10

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
}, "model.ckpt")
