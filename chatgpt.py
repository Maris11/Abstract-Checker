from chatgpt_wrapper import ChatGPT
import csv

ai = ChatGPT()
ai.refresh_session()
file = open('abstracts.csv', 'r', encoding='utf-8')
reader = csv.reader(file)
titles = []
rows = list(reader)
row_id = int(rows[-1][0]) + 1

for i in range(300, 400):
    titles.append(rows[i][1])

file.close()
file = open('abstracts.csv', 'a', encoding='utf-8', newline='')
writer = csv.writer(file)

for title in titles:
    print(title)
    response = ai.ask("Uzraksti anotāciju (līdz 850 rakstzīmēm) kvalifikācijas vai kursa vai bakalaura vai maģistra "
                      "darba tēmai \"" + title + "\". Izmanto atšķirīgus vārdus un struktūru "
                                                 "nekā iepriekš.")
    response = '\n'.join([line for line in response.splitlines() if line.strip()])
    print(response)
    writer.writerow([row_id, title, response, 1])
    row_id = row_id + 1
