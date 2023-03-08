import torch
import string
import torch.nn as nn
import pandas as pd
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
from torch.utils.data import DataLoader, TensorDataset, random_split

abstracts = pd.read_csv(
    "abstracts_test.csv",
    delimiter=',',
    encoding='utf-8',
    header=0
)
abstracts = abstracts.fillna("")  # nomaina tukšās vērtības ar tukšu string
abstracts.abstract = abstracts.abstract.str.replace('[{}]'.format(string.punctuation), '')  # noņem pieturzīmes
tokenizer = get_tokenizer(tokenizer=None, language='lv')  # tokenaizers
abstract_text = [tokenizer(text) for text in abstracts.abstract]  # atsaukmju teksta tokenēšana
vocab_text = build_vocab_from_iterator(iter(abstract_text), specials=["<unk>", "<pad>"])  # izveido teksta vārdnīcu
vocab_text.set_default_index(vocab_text["<unk>"])
abstract_text = [torch.tensor(vocab_text(tokens)) for tokens in abstract_text]  # pārveido par tenzoriem
abstract_text = torch.nn.utils.rnn.pad_sequence(abstract_text, padding_value=vocab_text['<pad>'], batch_first=True)
generated = torch.tensor(abstracts.is_generated, dtype=torch.float)

dataset = TensorDataset(abstract_text, generated)

train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=True)

print(vocab_text['saspiešanas'])
print(len(train_loader))
print(len(test_loader))

EMBEDDING_SIZE = 5
VOCAB_LENGTH = len(vocab_text)
TEXT_SEQUENCE_LENGTH = len(abstract_text[0])


class IsGenerated(nn.Module):
    def __init__(self):
        super().__init__()

        self.abs = nn.Sequential(
            nn.Embedding(VOCAB_LENGTH, EMBEDDING_SIZE),
            nn.Flatten(),
            nn.Linear(in_features=EMBEDDING_SIZE * TEXT_SEQUENCE_LENGTH, out_features=32),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=1),
            nn.Sigmoid()
        )

    def forward(self, text):
        is_generated = self.abs(text)

        return is_generated


model = IsGenerated()
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

correct_true = 0
correct_false = 0
true_count = 0
false_count = 0

for text, generated in test_loader:
    out = model(text)

    is_correct = torch.round(out[0])[0] == generated[0]

    if generated[0] == 1:
        true_count = true_count + 1
    else:
        false_count = false_count + 1

    if is_correct:
        if generated[0] == 1:
            correct_true = correct_true + 1
        else:
            correct_false = correct_false + 1

print("True Precision: {:.1f}%\nFalse Precision: {:.1f}%\nOverall precision: {:.1f}%".format(
    correct_true / true_count * 100,
    correct_false / false_count * 100,
    correct_false + correct_true / len(test_loader)
))
