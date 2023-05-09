import csv
import pandas as pd
import stanza

stanza.download(lang="lv", processors='tokenize')
nlp = stanza.Pipeline(lang='lv', processors='tokenize')

language = 'english'
faculties = ['bio', 'bme', 'df', 'fmo', 'geo', 'hzf', 'law', 'med', 'ppm']
real = True

for faculty in faculties:
    abstracts = pd.read_csv(
        "abstracts/" + language + "/" + faculty + "_abstracts_" + ("real" if real else "generated") + ".csv",
        delimiter=',',
        encoding='utf-8',
        header=0,
        usecols=['abstract', 'is_generated']
    )

    abstracts = abstracts.fillna("")

    file = open("abstracts/" + language + "/sentences/" + faculty + "_sentences_" + ("real" if real else "generated") + ".csv", 'w', encoding='utf-8', newline='\n')
    writer = csv.writer(file)
    writer.writerow(['id', 'sentence', 'is_generated'])
    sentence_id = 1

    for i, row in abstracts.iterrows():
        new_rows = []
        abstract = row['abstract']
        is_generated = row['is_generated']
        sentences = nlp(abstract)

        for sentence in sentences.sentences:
            new_rows.append([sentence_id, sentence.text, is_generated])
            sentence_id = sentence_id + 1

        writer.writerows(new_rows)

        if (i + 1) % 100 == 0:
            print('{}/{}'.format(i + 1, len(abstracts)))
