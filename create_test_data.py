import csv
import pandas as pd
import stanza
import Constants

language = Constants.LANGUAGE

stanza.download(lang="lv" if language == "latvian" else "en", processors='tokenize')
nlp = stanza.Pipeline(lang="lv" if language == "latvian" else "en", processors='tokenize')

language = 'english'
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
file = open("data/" + language + "/abstract_test_data.csv", 'w', encoding='utf-8', newline='\n')
abstract_writer = csv.writer(file)
abstract_writer.writerow(['id', 'abstract', 'is_generated'])
file = open("data/" + language + "/sentence_test_data.csv", 'w', encoding='utf-8', newline='\n')
sentence_writer = csv.writer(file)
sentence_writer.writerow(['sentence', 'is_generated'])
new_real_sentences = []
new_generated_sentences = []
abstract_id = 1

for faculty in faculties:
    abstracts_real = pd.read_csv(
        "abstracts/" + language + "/" + faculty + "_abstracts_real.csv",
        delimiter=',',
        encoding='utf-8',
        header=0,
        usecols=['abstract', 'is_generated']
    )

    abstracts_real = abstracts_real.tail(56)

    abstracts_generated = pd.read_csv(
        "abstracts/" + language + "/" + faculty + "_abstracts_generated.csv",
        delimiter=',',
        encoding='utf-8',
        header=0,
        usecols=['abstract', 'is_generated']
    )

    abstracts_generated = abstracts_generated.tail(56)
    abstracts = pd.concat([abstracts_generated, abstracts_real], axis=0, ignore_index=True)

    for i, row in abstracts.iterrows():
        abstract = row['abstract']
        is_generated = row['is_generated']
        abstract_writer.writerow([abstract_id, abstract, is_generated])
        abstract_id = abstract_id + 1
        sentences = nlp(abstract)

        for sentence in sentences.sentences:
            if is_generated:
                new_generated_sentences.append([sentence.text, is_generated])
            else:
                new_real_sentences.append([sentence.text, is_generated])

while len(new_real_sentences) > 1900:
    new_real_sentences.pop()

while len(new_generated_sentences) > 1900:
    new_generated_sentences.pop()

sentence_writer.writerows(new_real_sentences)
sentence_writer.writerows(new_generated_sentences)
