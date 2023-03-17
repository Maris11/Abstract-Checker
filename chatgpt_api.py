import openai
import Constants
import csv

openai.api_key = Constants.OPENAI_API_KEY

file = open('abstracts/bme_abstracts_real.csv', 'r', encoding='utf-8')
reader = csv.reader(file)
titles = []
rows = list(reader)
row_id = 253

for i in range(row_id - 1, 1902):
    titles.append(rows[i][1])

file.close()
file = open('abstracts/bme_abstracts_generated.csv', 'a', encoding='utf-8', newline='')
writer = csv.writer(file)

for title in titles:
    print(title)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Tu ģenerē anotācijas pētnieciskajiem darbiem no to nosaukuma. Līdz 850 rakstzīmēm. "
                        "Izmantot tagadnes formu. Anotācijas sākumu izvēlies kā random darba veidu (bakalaura, "
                        "maģistra, kursa, dilpomdarbs vai citu) vai vispār to nemini un izvēlies random sākuma "
                        "formātu. Nerakstīt tekstā, ka tā ir anotācija."},
            {"role": "user",
             "content": "Nosaukums \"" + title + "\""}
        ]
    )

    response = response['choices'][0]['message']['content']
    response = response.replace('\n', '')
    print(response)
    writer.writerow([row_id, title, response, 1])
    row_id = row_id + 1
