import time
import openai
import Constants
import csv

openai.api_key = Constants.OPENAI_API_KEY

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
language = Constants.LANGUAGE

for faculty in faculties:
    file = open('abstracts/' + language + '/' + faculty + '_abstracts_real.csv', 'r', encoding='utf-8')
    reader = csv.reader(file)
    titles = []
    rows = list(reader)
    row_id = 1

    for i in range(row_id, len(rows)):
        titles.append(rows[i][1])

    file.close()
    file = open('abstracts/' + language + '/' + faculty + '_abstracts_generated.csv', 'a', encoding='utf-8', newline='')
    writer = csv.writer(file)

    if row_id == 1:
        writer.writerow(['id', 'title', 'abstract', 'is_generated'])

    for title in titles:
        print(title)
        error = True

        while error:
            error = False

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user",
                         "content": "Write a random abstract for something with a title of \"" + title + "\". Write in "
                                    + language + "! Don't mention the title. "
                                    "Write only the abstract and don't mention that it is an abstract"
                         }
                    ]
                )
            except:
                time.sleep(10)
                error = True

        response = response['choices'][0]['message']['content']
        response = response.replace('\n', '')
        print(response)
        writer.writerow([row_id, title, response, 1])
        row_id = row_id + 1
