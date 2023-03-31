import torch
import string
import torch.nn as nn
import pandas as pd
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
from torch.utils.data import DataLoader, TensorDataset, random_split

real = pd.read_csv(
    "abstracts/bme_abstracts_real.csv",
    delimiter=',',
    encoding='utf-8',
    header=0,
    usecols=['abstract', 'is_generated']
)

generated = pd.read_csv(
    "abstracts/bme_abstracts_generated.csv",
    delimiter=',',
    encoding='utf-8',
    header=0,
    usecols=['abstract', 'is_generated']
)

abstracts = pd.concat([real, generated], axis=0, ignore_index=True)
abstracts = abstracts.fillna("")  # nomaina tukšās vērtības ar tukšu string
abstracts.abstract = abstracts.abstract.str.replace('[{}]'.format(string.punctuation), '')  # noņem pieturzīmes
tokenizer = get_tokenizer(tokenizer=None, language='lv')  # tokenaizers
abstract_text = [tokenizer(text) for text in abstracts.abstract]  # atsaukmju teksta tokenēšana
vocabulary = build_vocab_from_iterator(iter(abstract_text), specials=["<unk>", "<pad>"])  # izveido teksta vārdnīcu
vocabulary.set_default_index(vocabulary["<unk>"])
abstract_text = [torch.tensor(vocabulary(tokens)) for tokens in abstract_text]  # pārveido par tenzoriem
abstract_text = torch.nn.utils.rnn.pad_sequence(abstract_text, padding_value=vocabulary['<pad>'], batch_first=True)
generated = torch.tensor(abstracts.is_generated, dtype=torch.float)

torch.save(vocabulary, 'vocabulary.pth')

dataset = TensorDataset(abstract_text, generated)
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=True)


class IsGenerated(nn.Module):
    def __init__(self, embedding_size, vocab_length, text_sequence_size):
        super().__init__()

        self.abs = nn.Sequential(
            nn.Embedding(vocab_length, embedding_size),
            nn.Flatten(),
            nn.Linear(in_features=embedding_size * text_sequence_size, out_features=32),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=1),
            nn.Sigmoid()
        )

    def forward(self, text):
        is_generated = self.abs(text)

        return is_generated


print(len(abstract_text[0]), len(vocabulary))

model = IsGenerated(5, len(vocabulary), len(abstract_text[0]))
loss_fn = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
num_epochs = 10
loss = None

for epoch in range(num_epochs):
    model.train()

    for text, generated in train_loader:
        prediction = model(text).squeeze(1)
        loss = loss_fn(prediction, generated)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch + 1, num_epochs, loss.item()))

correct_generated = 0
correct_real = 0
generated_count = 0
real_count = 0

for text, generated in test_loader:
    out = model(text)
    is_correct = torch.round(out[0])[0] == generated[0]

    if generated[0] == 1:
        generated_count = generated_count + 1
    else:
        real_count = real_count + 1

    if is_correct:
        if generated[0] == 1:
            correct_generated = correct_generated + 1
        else:
            correct_real = correct_real + 1

print("Generated Precision: {:.1f}%\nReal Precision: {:.1f}%\nOverall precision: {:.1f}%".format(
    correct_generated / generated_count * 100,
    correct_real / real_count * 100,
    (correct_real + correct_generated) / len(test_loader) * 100
))

state_dict = model.state_dict()
torch.save(state_dict, "model.tar")
