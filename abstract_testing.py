generated_threshold = 50
tp = 0
tn = 0
fp = 0
fn = 0

with open('test_data/test_generated_abstract_probabilites.csv', 'r') as file:
    for row in file:
        is_correct = float(row) >= generated_threshold

        if is_correct:
            tp = tp + 1
        else:
            fp = fp + 1

with open('test_data/test_real_abstract_probabilites.csv', 'r') as file:
    for row in file:
        is_correct = float(row) < generated_threshold

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