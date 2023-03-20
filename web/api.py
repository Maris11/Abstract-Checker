import torch
from torch import nn
from torchtext.data.utils import get_tokenizer
import string

def application(environ, start_response):
    # Check that the request method is POST
    if environ['REQUEST_METHOD'] != 'POST':
        start_response('405 Method Not Allowed', [('Content-type', 'text/plain')])
        return [b'Only POST requests are allowed.']

    # Read the request body and decode it as a UTF-8 string
    request_body = environ['wsgi.input'].read().decode('utf-8')

    # Print the request body to the console for debugging purposes
    print(request_body)

    # Set the response headers
    status = '200 OK'
    response_body = predict_abstract(request_body)
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(response_body))),
                        ('Access-Control-Allow-Origin', '*'),
                        ('Access-Control-Allow-Methods', 'POST'),
                        ('Access-Control-Allow-Headers', 'Content-Type')]

    # Send the response back to the client
    start_response(status, response_headers)
    return [response_body.encode('utf-8')]

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


def predict_abstract(abstract):
    vocabulary = torch.load('vocabulary.pth')

    # Data preprocessing steps
    tokenizer = get_tokenizer(tokenizer=None, language='lv')
    abstract = abstract.replace('[{}]'.format(string.punctuation), '')
    abstract = torch.tensor(vocabulary(tokenizer(abstract)), dtype=torch.long).unsqueeze(0)
    abstract = torch.nn.utils.rnn.pad_sequence(abstract, padding_value=vocabulary['<pad>'], batch_first=True)
    abstract = torch.nn.functional.pad(abstract, (0, 437 - len(abstract[0])), mode='constant')

    model = IsGenerated(5, len(vocabulary), len(abstract[0]))
    model.load_state_dict(torch.load("model.tar"))

    return f"{100*model(abstract).item():.1f}%"
