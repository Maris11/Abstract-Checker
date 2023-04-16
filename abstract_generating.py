import time

import openai
import Constants
import csv

openai.api_key = Constants.OPENAI_API_KEY

file = open('abstracts/hzf_abstracts_real.csv', 'r', encoding='utf-8')
reader = csv.reader(file)
titles = []
rows = list(reader)
row_id = 500

for i in range(row_id, 501):
    titles.append(rows[i][1])

file.close()
file = open('abstracts/hzf_abstracts_generated.csv', 'a', encoding='utf-8', newline='')
writer = csv.writer(file)

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
                     "content": "Uzraksti anotāciju tēmai \"" + title + "\""
                     }
                ]
            )
        except openai.error.RateLimitError:
            time.sleep(10)
            error = True

    response = response['choices'][0]['message']['content']
    response = response.replace('\n', '')
    print(response)
    writer.writerow([row_id, title, response, 1])
    row_id = row_id + 1
