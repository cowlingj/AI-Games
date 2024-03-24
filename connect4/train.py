import sys
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

rng = np.random.default_rng()

dataset = rng.permutation(np.loadtxt('data.csv', delimiter=',', dtype=np.int8))
X = torch.tensor(dataset[:,0:42], dtype=torch.float32)
y = torch.tensor(dataset[:,42:49], dtype=torch.float32)

hidden_size = 1024
hidden_count = 6
layers = [ nn.Linear(X.shape[1], hidden_size), nn.ReLU() ] + \
    [ x for xs in [ [nn.Linear(hidden_size, hidden_size), nn.ReLU()] for _ in range(hidden_count) ] for x in xs ] + \
    [ nn.Linear(hidden_size, y.shape[1]), nn.Sigmoid()]

model = nn.Sequential(
    *layers
)

training_size = 400
X_train = X[0:training_size]
y_train = y[0:training_size]

X_test = X[training_size:-1]
y_test = y[training_size:-1]

if sys.argv[1] == "train":
    loss_fn = nn.BCELoss()  # binary cross entropy
    optimizer = optim.Adam(model.parameters(), lr=0.0006)

    n_epochs = 100
    batch_size = 10

    for epoch in range(n_epochs):
        for i in range(0, len(X_train), batch_size):
            Xbatch = X_train[i:i+batch_size]
            y_pred = model(Xbatch)
            ybatch = y_train[i:i+batch_size]
            loss = loss_fn(y_pred, ybatch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        print(f'Finished epoch {epoch}, latest loss {loss}')
    torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss,
    }, "model.ckpt")

if sys.argv[1] == "test":
    with torch.no_grad():
        model.load_state_dict(torch.load('model.ckpt')['model_state_dict'])
        model.eval()
        y_pred = np.array(model(X_test))
        rounded = np.where(y_pred == np.max(y_pred, axis=1).reshape(-1, 1), 1, 0)

        accuracy = np.all((rounded == np.array(y_test)), axis=1).mean()
        print(f"Accuracy {accuracy}")
