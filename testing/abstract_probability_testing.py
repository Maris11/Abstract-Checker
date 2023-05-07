import csv
import pandas as pd
from predict_from_abstract import split_into_sentences, predict_sentences

abstracts = pd.read_csv(
    "../data/abstract_test_data.csv",
    delimiter=',',
    encoding='utf-8',
    header=0,
    usecols=['abstract', 'is_generated']
)

file_real = open('../data/test_real_abstract_probabilites.csv', 'w', encoding='utf-8', newline='\n')
writer_real = csv.writer(file_real)
file_generated = open('../data/test_generated_abstract_probabilites.csv', 'w', encoding='utf-8', newline='\n')
writer_generated = csv.writer(file_generated)

for i, row in abstracts.iterrows():
    sentences = split_into_sentences(row.abstract)
    probs = predict_sentences(sentences)
    probs = [float(val) for val in probs]
    probability = round(sum(probs) / len(probs), 1)
    if row.is_generated:
        writer_generated.writerow([round(probability, 1)])
    else:
        writer_real.writerow([round(probability, 1)])

    print('{}/{}'.format(i + 1, len(abstracts)))
