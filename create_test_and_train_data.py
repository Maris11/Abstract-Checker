import csv
import pandas as pd

faculties = ['bme', 'df', 'hzf']

real = []
generated = []
train_pct = 0.8  # 80% for training
test_pct = 0.2   # 20% for testing
nrows = 2000

for faculty in faculties:
    faculty_sentences = pd.read_csv(
        "abstracts/" + faculty + "_sentences_generated.csv",
        delimiter=',',
        encoding='utf-8',
        header=0,
        nrows=nrows
    )
    generated.append(faculty_sentences)
    faculty_sentences = pd.read_csv(
        "abstracts/" + faculty + "_sentences_real.csv",
        delimiter=',',
        encoding='utf-8',
        header=0,
        nrows=nrows
    )
    real.append(faculty_sentences)

real = pd.concat(real, axis=0, ignore_index=True)
generated = pd.concat(generated, axis=0, ignore_index=True)

split_index = int(train_pct * len(real))
train_sentences_real = real[:split_index]
test_sentences_real = real[split_index:]

train_sentences_generated = generated[:split_index]
test_sentences_generated = generated[split_index:]

train_sentences = pd.concat([train_sentences_generated, train_sentences_real], axis=0, ignore_index=True)
test_sentences = pd.concat([test_sentences_generated, test_sentences_real], axis=0, ignore_index=True)

file = open('abstracts/train_data.csv', 'w', encoding='utf-8', newline='\n')
writer = csv.writer(file)
writer.writerow(['sentence', 'is_generated'])

for i, row in train_sentences.iterrows():
    writer.writerow([row.sentence, row.is_generated])

file.close()

file = open('abstracts/test_data.csv', 'w', encoding='utf-8', newline='\n')
writer = csv.writer(file)
writer.writerow(['sentence', 'is_generated'])

for i, row in test_sentences.iterrows():
    writer.writerow([row.sentence, row.is_generated])
