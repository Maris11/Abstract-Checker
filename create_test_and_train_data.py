import csv
import pandas as pd

faculties = ['bme', 'df']

sentences = []

for faculty in faculties:
    faculty_sentences = pd.read_csv(
        "abstracts/" + faculty + "_sentences.csv",
        delimiter=',',
        encoding='utf-8',
        header=0
    )
    sentences.append(faculty_sentences.sample(n=18000))

sentences = pd.concat(sentences, axis=0, ignore_index=True)
sentences = sentences.sample(frac=1).reset_index(drop=True)
train_pct = 0.8  # 80% for training
test_pct = 0.2   # 20% for testing
split_index = int(train_pct * len(sentences))
train_sentences = sentences[:split_index]
test_sentences = sentences[split_index:]

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
