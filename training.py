import torch
import torch.nn as nn
import pandas as pd
from Module import create_data_loader_and_model

device = torch.device('cuda')
torch.manual_seed(42)

sentences = pd.read_csv(
    "train_data.csv",
    delimiter=',',
    encoding='utf-8',
    header=0
)

data_loader, model = create_data_loader_and_model(sentences, save_vocab=True, batch_size=32, embedding_dim=200)

loss_fn = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
num_epochs = 15
loss = None

for epoch in range(num_epochs):
    for text, generated in data_loader:
        optimizer.zero_grad()
        prediction = model(text).squeeze()
        loss = loss_fn(prediction, generated)
        loss.backward()
        optimizer.step()

    print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch + 1, num_epochs, loss.item()))

torch.save(model.state_dict(), "model.tar")
