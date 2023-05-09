from bs4 import BeautifulSoup
import requests
import warnings
import csv

warnings.filterwarnings('ignore', message='Unverified HTTPS request is being made')

language = 'english'
faculties = ['bio', 'bme', 'df', 'fmo', 'geo', 'hzf', 'law', 'med', 'ppm']
ids = [5278, 5280, 5279, 5281, 5282, 5283, 5284, 5285, 4425]
offsets = [164, 630, 474, 213, 147, 442, 600, 491, 2500]
amount = 200

for i in range(len(faculties)):
    print(faculties[i])
    offset = offsets[i]
    row_id = 1
    file = open('abstracts/' + language + '/' + faculties[i] + '_abstracts_real.csv', 'a', encoding='utf-8', newline='\n')
    writer = csv.writer(file)
    writer.writerow(['id', 'title', 'abstract', 'is_generated'])

    for j in range(int(amount / 20)):
        response = requests.get('https://dspace.lu.lv/dspace/handle/7/' + str(ids[i]) + '/recent-submissions?'
                                                                                        'offset=' + str(offset),
                                verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        links_with_title = soup.select('h4>a')
        links = [a['href'] for a in links_with_title]
        titles = [a.string for a in links_with_title]
        abstracts = []
        rows = []

        for link in links:
            response = requests.get('https://dspace.lu.lv' + link, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            abstract = soup.select_one('.simple-item-view-description>div')

            if abstract is None:
                continue
            else:
                text = abstract.get_text(separator='<').split(sep='<')

                if len(text) <= 2 or len(text[2]) < 200:
                    continue
                else:
                    text = text[2 if language == 'english' else 0]

            abst = text.replace('\n', '')
            abstracts.append(abst)

        for k in range(len(abstracts)):
            rows.append([row_id, titles[k], abstracts[k], 0])
            row_id = row_id + 1

        writer.writerows(rows)
        offset = offset + 20
        print('{}/{}'.format((j + 1) * 20, amount))
