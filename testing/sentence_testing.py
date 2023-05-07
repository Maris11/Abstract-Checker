import pandas as pd
from model import create_data_loader_and_model

sentences = pd.read_csv(
    "../data/sentence_test_data.csv",
    delimiter=',',
    encoding='utf-8',
    header=0
)

data_loader, model = create_data_loader_and_model(sentences, model_path="../model.pt")
generated_threshold = 0.5
tp = 0
tn = 0
fp = 0
fn = 0

for text, generated in data_loader:
    out = model(text)

    if generated[0] == 1:
        is_correct = out >= generated_threshold

        if is_correct:
            tp = tp + 1
        else:
            fp = fp + 1
    else:
        is_correct = out < generated_threshold

        if is_correct:
            tn = tn + 1
        else:
            fn = fn + 1

print(tp, tn, fp, fn)

accuracy = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1_score = 2 * (recall * precision) / (recall + precision)
specificity = tn / (tn + fp)

print(
    "Accuracy: {:.1f}%\n"
    "Precision: {:.1f}%\n"
    "Recall: {:.1f}%\n"
    "F1-score: {:.1f}%\n"
    "Specificity: {:.1f}%\n"
    .format(
        accuracy * 100,
        precision * 100,
        recall * 100,
        f1_score * 100,
        specificity * 100
    )
)
