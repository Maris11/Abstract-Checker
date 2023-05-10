import csv
import pandas as pd
import Constants
from predict_from_abstract import split_into_sentences, predict_sentences

language = Constants.LANGUAGE

abstracts = pd.read_csv(
    "../data/" + language + "/abstract_test_data.csv",
    delimiter=',',
    encoding='utf-8',
    header=0,
    usecols=['abstract', 'is_generated']
)

file_real = open("../data/" + language + "/test_real_abstract_probabilites.csv", 'w', encoding='utf-8', newline='\n')
writer_real = csv.writer(file_real)
file_generated = open("../data/" + language + "/test_generated_abstract_probabilites.csv", 'w', encoding='utf-8', newline='\n')
writer_generated = csv.writer(file_generated)

for i, row in abstracts.iterrows():
    sentences = split_into_sentences(row.abstract, language)
    probs = predict_sentences(sentences, language, model_path="../model_" + language + ".pt")
    all_word_count = 0
    average = 0
    j = 0

    for sentence in sentences:
        word_count = len(sentence.split())
        all_word_count = all_word_count + word_count
        average = average + float(probs[j]) * word_count
        j = j + 1

    total_probability = round(average / all_word_count, 1)

    if row.is_generated:
        writer_generated.writerow([total_probability])
    else:
        writer_real.writerow([total_probability])

    print('{}/{}'.format(i + 1, len(abstracts)))
