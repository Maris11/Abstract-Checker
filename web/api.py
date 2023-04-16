import torch
import json
import pandas as pd
import string
import stanza

from Module import create_data_loader_and_model

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


def predict_sentences(sentences: list) -> list:
    sentences = pd.DataFrame(sentences, columns=['sentence'])
    with open("model.bin", "r") as f:
        seq_size = int(f.read())

    data_loader, model = create_data_loader_and_model(sentences, with_is_generated=False, text_sequence_size=seq_size)
    model.load_state_dict(torch.load("model.tar"))
    model = model.to(device)

    percentages = []

    for sentence in data_loader:
        sentence = sentence[0]
        percentages.append(f"{100 * model(sentence).item():.1f}")

    return percentages
