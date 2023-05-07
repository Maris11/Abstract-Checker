import pandas as pd
import string
import stanza
from model import create_data_loader_and_model

stanza.download(lang="lv", processors='tokenize')
nlp = stanza.Pipeline(lang='lv', processors='tokenize')


def split_into_sentences(text: string) -> list:
    sentences = nlp(text)
    sentences = [sentence.text for sentence in sentences.sentences]

    return sentences


def predict_sentences(sentences: list) -> list:
    sentences = pd.DataFrame(sentences, columns=['sentence'])
    data_loader, model = create_data_loader_and_model(sentences, with_is_generated=False, shuffle=False)
    percentages = []

    for sentence in data_loader:
        sentence = sentence[0]
        percentages.append(f"{100 * model(sentence).item():.1f}")

    return percentages
