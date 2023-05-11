import pandas as pd
import Constants
from model import create_data_loader_and_model
from print_metrics import print_metrics

language = Constants.LANGUAGE

sentences = pd.read_csv(
    "../data/" + language + "/sentence_test_data.csv",
    delimiter=',',
    encoding='utf-8',
    header=0
)

data_loader, model = create_data_loader_and_model(
    sentences,
    language=language,
    model_path="../model_" + language + ".pt"
)

tp = 0
tn = 0
fp = 0
fn = 0

for text, generated in data_loader:
    out = model(text)

    if generated[0] == 1:
        is_correct = out >= 0.5

        if is_correct:
            tp = tp + 1
        else:
            fp = fp + 1
    else:
        is_correct = out < 0.5

        if is_correct:
            tn = tn + 1
        else:
            fn = fn + 1

print_metrics(tp, tn, fp, fn)
