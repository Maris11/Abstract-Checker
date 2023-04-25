import csv
import pandas as pd
import torch
from web.api import split_into_sentences, predict_sentences

device = torch.device('cuda')
torch.manual_seed(42)

abstracts = pd.read_csv(
    "test_data/abstract_test_data.csv",
    delimiter=',',
    encoding='utf-8',
    header=0,
    usecols=['abstract', 'is_generated']
)

file_real = open('test_data/test_real_abstract_probabilites.csv', 'w', encoding='utf-8', newline='\n')
writer_real = csv.writer(file_real)
file_generated = open('test_data/test_generated_abstract_probabilites.csv', 'w', encoding='utf-8', newline='\n')
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
