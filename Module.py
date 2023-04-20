import string

import pandas as pd
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
from torchtext.data import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator

device = torch.device('cuda')
torch.manual_seed(42)


class IsGenerated(nn.Module):
    def __init__(self, embedding_dim, vocab_size, text_sequence_size):
        super(IsGenerated, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, text_sequence_size, batch_first=True)
        self.linear = nn.Linear(text_sequence_size, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, sentences):
        embedded = self.embedding(sentences)
        output, (hidden, cell) = self.lstm(embedded)
        last_hidden = hidden[-1]
        logits = self.linear(last_hidden)
        logits = self.sigmoid(logits)
        return logits


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def create_data_loader_and_model(
        sentences: pd.DataFrame,
        save_vocab: bool = False,
        batch_size: int = 1,
        with_is_generated: bool = True,
        text_sequence_size: int = 0,
        shuffle: bool = True,
        embedding_dim: int = 100
):
    sentences = sentences.fillna("")
    sentences.sentence = sentences.sentence.apply(lambda x: remove_punctuation(x))
    tokenizer = get_tokenizer(tokenizer=None, language='lv')
    sentence_text = [tokenizer(text) for text in sentences.sentence]

    if save_vocab:
        vocabulary = build_vocab_from_iterator(iter(sentence_text),
                                               specials=["<unk>", "<pad>"])
        vocabulary.set_default_index(vocabulary["<unk>"])
        torch.save(vocabulary, 'vocabulary.pth')
    else:
        vocabulary = torch.load('vocabulary.pth')

    sentence_text = [torch.tensor(vocabulary(tokens)).to(device) for tokens in sentence_text]
    sentence_text = torch.nn.utils.rnn.pad_sequence(sentence_text, padding_value=vocabulary['<pad>'], batch_first=True)

    if not text_sequence_size:
        with open("model.bin", "w") as f:
            f.write(str(len(sentence_text[0])))

    if with_is_generated:
        generated = torch.tensor(sentences.is_generated, dtype=torch.float).to(device)
        dataset = TensorDataset(sentence_text, generated)
    else:
        dataset = TensorDataset(sentence_text)

    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

    model = IsGenerated(embedding_dim, len(vocabulary), text_sequence_size if text_sequence_size else len(sentence_text[0])).to(device)

    return data_loader, model.to(device)
