import csv
import pandas as pd
import stanza

stanza.download(lang="lv", processors='tokenize')
nlp = stanza.Pipeline(lang='lv', processors='tokenize')

real = pd.read_csv(
    "abstracts/df_abstracts_real.csv",
    delimiter=',',
    encoding='utf-8',
    header=0,
    usecols=['abstract', 'is_generated']
)

generated = pd.read_csv(
    "abstracts/df_abstracts_generated.csv",
    delimiter=',',
    encoding='utf-8',
    header=0,
    usecols=['abstract', 'is_generated']
)

abstracts = pd.concat([real, generated], axis=0, ignore_index=True)
abstracts = abstracts.fillna("")

file = open('abstracts/df_sentences.csv', 'a', encoding='utf-8', newline='\n')
writer = csv.writer(file)

for i, row in abstracts.iterrows():
    new_rows = []
    abstract = row['abstract']
    is_generated = row['is_generated']
    sentences = nlp(abstract)

    for sentence in sentences.sentences:
        new_rows.append([sentence.text, is_generated])

    writer.writerows(new_rows)
    if (i + 1) % 20 == 0:
        print('{}/{}'.format(i + 1, len(abstracts)))
