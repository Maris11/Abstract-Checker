import torch
import json
from torch import nn
from torchtext.data.utils import get_tokenizer
import string
import stanza

stanza.download(lang="lv", processors='tokenize')
nlp = stanza.Pipeline(lang='lv', processors='tokenize')
device = torch.device('cuda')

def application(environ, start_response):
    # Check that the request method is POST
    if environ['REQUEST_METHOD'] != 'POST':
        start_response('405 Method Not Allowed', [('Content-type', 'text/plain')])
        return [b'Only POST requests are allowed.']

    # Read the request body and decode it as a UTF-8 string
    request_body = environ['wsgi.input'].read().decode('utf-8')

    sentences = split_into_sentences(request_body)
    percentages = predict_sentences(sentences)

    # Set the response headers
    status = '200 OK'
    response_body = json.dumps([sentences, percentages])
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(response_body))),
                        ('Access-Control-Allow-Origin', '*'),
                        ('Access-Control-Allow-Methods', 'POST'),
                        ('Access-Control-Allow-Headers', 'Content-Type')]

    # Send the response back to the client
    start_response(status, response_headers)
    return [response_body.encode('utf-8')]


def split_into_sentences(text: string) -> list:
    sentences = nlp(text)
    sentences = [sentence.text for sentence in sentences.sentences]

    return sentences


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


def predict_sentences(sentences: list) -> list:
    vocabulary = torch.load('vocabulary.pth')
    tokenizer = get_tokenizer(tokenizer=None, language='lv')
    model = IsGenerated(5, len(vocabulary), 133)
    model.load_state_dict(torch.load("model.tar"))
    model = model.to(device)
    percentages = []

    for sentence in sentences:
        sentence = sentence.replace('[{}]'.format(string.punctuation), '')
        sentence = torch.tensor(vocabulary(tokenizer(sentence)), dtype=torch.long).to(device).unsqueeze(0)
        sentence = torch.nn.utils.rnn.pad_sequence(sentence, padding_value=vocabulary['<pad>'], batch_first=True)
        sentence = torch.nn.functional.pad(sentence, (0, 133 - len(sentence[0])), mode='constant')
        percentages.append(f"{100 * model(sentence).item():.1f}")

    return percentages
