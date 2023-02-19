from chatgpt_wrapper import ChatGPT
import csv

ai = ChatGPT()
file = open('abstracts.csv', 'r', encoding='utf-8')
reader = csv.reader(file)
titles = []
rows = list(reader)
row_id = rows[-1][0] + 1

for i, row in enumerate(reader):
    if i == 100:
        break
    titles.append(row[1])

file = open('abstracts.csv', 'a', encoding='utf-8')
writer = csv.writer(file)

for title in titles:
    response = ai.ask("Uzraksti anotāciju zinātniski pētnieciksajam darbam ar tēmu \"" + title + "\".")
    writer.writerow([row_id, title, response, 1])
    row_id = row_id + 1
