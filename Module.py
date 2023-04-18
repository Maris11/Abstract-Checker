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


def create_data_loader_and_model(
        sentences: pd.DataFrame,
        save_vocab: bool = False,
        batch_size: int = 1,
        with_is_generated: bool = True,
        text_sequence_size: int = 0,
        shuffle: bool = True
):
    sentences = sentences.fillna("")  # nomaina tukšās vērtības ar tukšu string
    sentences.sentence = sentences.sentence.str.replace('[{}]'.format(string.punctuation), '')  # noņem pieturzīmes
    tokenizer = get_tokenizer(tokenizer=None, language='lv')  # tokenaizers
    sentence_text = [tokenizer(text) for text in sentences.sentence]  # atsaukmju teksta tokenēšana

    if save_vocab:
        vocabulary = build_vocab_from_iterator(iter(sentence_text),
                                               specials=["<unk>", "<pad>"])  # izveido teksta vārdnīcu
        vocabulary.set_default_index(vocabulary["<unk>"])
        torch.save(vocabulary, 'vocabulary.pth')
    else:
        vocabulary = torch.load('vocabulary.pth')

    sentence_text = [torch.tensor(vocabulary(tokens)).to(device) for tokens in sentence_text]  # pārveido par tenzoriem
    sentence_text = torch.nn.utils.rnn.pad_sequence(sentence_text, padding_value=vocabulary['<pad>'], batch_first=True)

    if text_sequence_size and text_sequence_size > len(sentence_text[0]):
        # sentence_text = torch.nn.functional.pad(sentence_text, (0, text_sequence_size - len(sentence_text[0])), mode='constant')
        ones = torch.ones((sentence_text.shape[0], text_sequence_size - len(sentence_text[0])), dtype=sentence_text.dtype, device=sentence_text.device)
        sentence_text = torch.cat((sentence_text, ones), dim=1)
    elif text_sequence_size and text_sequence_size <= len(sentence_text[0]):
        sentence_text = sentence_text[:, :text_sequence_size - len(sentence_text[0])]
    else:
        with open("model.bin", "w") as f:
            f.write(str(len(sentence_text[0])))

    if with_is_generated:
        generated = torch.tensor(sentences.is_generated, dtype=torch.float).to(device)
        dataset = TensorDataset(sentence_text, generated)
    else:
        dataset = TensorDataset(sentence_text)

    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

    model = IsGenerated(5, len(vocabulary), text_sequence_size if text_sequence_size else len(sentence_text[0])).to(device)

    return data_loader, model.to(device)
