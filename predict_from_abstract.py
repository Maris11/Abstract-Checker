import pandas as pd
import string
import stanza
from model import create_data_loader_and_model

stanza.download(lang="en", processors='tokenize')
stanza.download(lang="lv", processors='tokenize')
nlp_en = stanza.Pipeline(lang="en", processors='tokenize')
nlp_lv = stanza.Pipeline(lang="lv", processors='tokenize')


def split_into_sentences(text: string, language: string) -> list:
    if language == "latvian":
        sentences = nlp_lv(text)
    else:
        sentences = nlp_en(text)

    sentences = [sentence.text for sentence in sentences.sentences]

    return sentences


def predict_sentences(sentences: list, language: string, model_path: string = '') -> list:
    sentences = pd.DataFrame(sentences, columns=['sentence'])
    data_loader, model = create_data_loader_and_model(
        sentences,
        with_is_generated=False,
        shuffle=False,
        language=language,
        model_path="model_" + language + ".pt" if not model_path else model_path
    )
    percentages = []

    for sentence in data_loader:
        sentence = sentence[0]
        percentages.append(f"{100 * model(sentence).item():.1f}")

    return percentages
