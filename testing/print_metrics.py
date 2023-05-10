def print_metrics(tp, tn, fp, fn):
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
