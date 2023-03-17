from bs4 import BeautifulSoup
import requests
import warnings
import csv

warnings.filterwarnings('ignore', message='Unverified HTTPS request is being made')

if __name__ == '__main__':
    offset = 700
    row_id = 1
    file = open('abstracts/bme_abstracts_real.csv', 'a', encoding='utf-8', newline='\n')
    writer = csv.writer(file)

    for i in range(100):
        response = requests.get('https://dspace.lu.lv/dspace/handle/7/72/browse?order=DESC&rpp=20&sort_by=2&etal=-1'
                                '&offset=' + str(offset) + '&type=dateissued', verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        links_with_title = soup.select('h4>a')
        links = [a['href'] for a in links_with_title]
        titles = [a.string for a in links_with_title]
        abstracts = []
        keywords = []
        rows = []

        for link in links:
            response = requests.get('https://dspace.lu.lv' + link, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            abstract = soup.select_one('.simple-item-view-description>div')

            if abstract is None:
                text = ''
            else:
                text = abstract.get_text(separator='<').split(sep='<')[0]

            if "Atslēgvārdi" in text:
                text = text.lower().split("atslēgvārdi")
                abst = text[0]
                keys = text[1]
            elif "Atslēgas vārdi" in text:
                text = text.lower().split("atslēgas vārdi")
                abst = text[0]
                keys = text[1]
            else:
                abst = text
                keys = ''

            abst = abst.replace('\n', '')
            keys = keys.replace(':', '')
            keys = keys.replace(' ', '')
            abstracts.append(abst)
            keywords.append(keys)

        # print(len(titles), titles)
        # print(len(abstracts), abstracts)
        # print(len(keywords), keywords)

        for j in range(len(abstracts)):
            rows.append([row_id, titles[j], abstracts[j], keywords[j], 0])
            row_id = row_id + 1

        writer.writerows(rows)
        offset = offset + 20
        print('{}/{}'.format((i+1)*20, 100*20))
