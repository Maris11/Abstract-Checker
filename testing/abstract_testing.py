import Constants
from print_metrics import print_metrics

language = Constants.LANGUAGE
generated_threshold = 50
tp = 0
tn = 0
fp = 0
fn = 0

with open("../data/" + language + "/test_generated_abstract_probabilites.csv", 'r') as file:
    for row in file:
        is_correct = float(row) >= generated_threshold

        if is_correct:
            tp = tp + 1
        else:
            fp = fp + 1

with open("../data/" + language + "/test_real_abstract_probabilites.csv", 'r') as file:
    for row in file:
        is_correct = float(row) < generated_threshold

        if is_correct:
            tn = tn + 1
        else:
            fn = fn + 1

print_metrics(tp, tn, fp, fn)
