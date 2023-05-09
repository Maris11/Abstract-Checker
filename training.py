import torch
import torch.nn as nn
import pandas as pd
import Constants
from model import create_data_loader_and_model

language = Constants.LANGUAGE
sentences = pd.read_csv(
    "data/" + language + "/train_data.csv",
    delimiter=',',
    encoding='utf-8',
    header=0
)

data_loader, model = create_data_loader_and_model(sentences, batch_size=32, load_model=False, language=language)
loss_fn = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
num_epochs = 100
loss = None

for epoch in range(num_epochs):
    for text, generated in data_loader:
        optimizer.zero_grad()
        prediction = model(text)
        loss = loss_fn(prediction, generated)
        loss.backward()
        optimizer.step()

    print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch + 1, num_epochs, loss.item()))

torch.save(model.state_dict(), "model_" + language + ".pt")
