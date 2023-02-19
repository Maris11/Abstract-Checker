from chatgpt_wrapper import ChatGPT
import csv

ai = ChatGPT()
file = open('abstracts.csv', 'r', encoding='utf-8')
reader = csv.reader(file)
titles = []
rows = list(reader)
row_id = int(rows[-1][0]) + 1

for i, row in enumerate(rows, start=32):
    if i == 100:
        break
    titles.append(row[1])

file.close()
file = open('abstracts.csv', 'a', encoding='utf-8', newline='')
writer = csv.writer(file)

for title in titles:
    response = ai.ask("Uzraksti anotāciju (līdz 850 rakstzīmēm) tēmai \"" + title + "\". Izmanto citādāku anotācijas struktūru.")
    response = '\n'.join([line for line in response.splitlines() if line.strip()])
    print(response)
    writer.writerow([row_id, title, response, 1])
    row_id = row_id + 1
