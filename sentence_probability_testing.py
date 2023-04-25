import csv
import pandas as pd
import torch
from Module import create_data_loader_and_model

device = torch.device('cuda')
torch.manual_seed(42)

sentences = pd.read_csv(
    "test_data/sentence_test_data.csv",
    delimiter=',',
    encoding='utf-8',
    header=0
)

data_loader, model = create_data_loader_and_model(sentences, shuffle=False)
model.load_state_dict(torch.load("model.tar"))
model = model.to(device)
i = 0
file_real = open('test_data/test_real_sentence_probabilities.csv', 'w', encoding='utf-8', newline='\n')
writer_real = csv.writer(file_real)
file_generated = open('test_data/test_generated_sentence_probabilities.csv', 'w', encoding='utf-8', newline='\n')
writer_generated = csv.writer(file_generated)

for text, generated in data_loader:
    out = model(text)

    if generated:
        writer_generated.writerow([round(out.item() * 100, 1)])
    else:
        writer_real.writerow([round(out.item() * 100, 1)])
    i = i + 1

    if i % 20 == 0:
        print('{}/{}'.format(i, len(sentences)))
