import csv
import pandas as pd
import Constants

language = Constants.LANGUAGE
faculties = [
    'bio',
    'bme',
    'df',
    'fmo',
    'geo',
    'hzf',
    'law',
    'med',
    'ppm'
]
real = []
generated = []
nrows_real = 500
nrows_generated = 500

for faculty in faculties:
    faculty_sentences = pd.read_csv(
        "abstracts/" + language + "/sentences/" + faculty + "_sentences_generated.csv",
        delimiter=',',
        encoding='utf-8',
        header=0,
        nrows=nrows_generated
    )
    generated.append(faculty_sentences)
    faculty_sentences = pd.read_csv(
        "abstracts/" + language + "/sentences/" + faculty + "_sentences_real.csv",
        delimiter=',',
        encoding='utf-8',
        header=0,
        nrows=nrows_real
    )
    real.append(faculty_sentences)

real = pd.concat(real, axis=0, ignore_index=True)
generated = pd.concat(generated, axis=0, ignore_index=True)
train_sentences = pd.concat([real, generated], axis=0, ignore_index=True)
file = open("data/" + language + "/train_data.csv", 'w', encoding='utf-8', newline='\n')
writer = csv.writer(file)
writer.writerow(['sentence', 'is_generated'])

for i, row in train_sentences.iterrows():
    word_count = len(row.sentence.split())

    if word_count < 4:
        continue

    writer.writerow([row.sentence, row.is_generated])
