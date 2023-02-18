from bs4 import BeautifulSoup
import requests
import warnings
import csv

warnings.filterwarnings('ignore', message='Unverified HTTPS request is being made')

if __name__ == '__main__':
    offset = 1240
    row_id = 641
    file = open('abstracts.csv', 'a', encoding='utf-8')
    writer = csv.writer(file)

    for i in range(113):
        response = requests.get('https://dspace.lu.lv/dspace/handle/7/5279/browse?order=DESC&rpp=20&sort_by=2&etal=-1'
                                '&offset=' + str(offset) + '&type=dateissued', verify=False)
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
                text = ''
            else:
                text = abstract.get_text(separator='<').split(sep='<')[0]
            abstracts.append(text)

        for j in range(len(abstracts)):
            rows.append([row_id, titles[j], abstracts[j], 0])
            row_id = row_id + 1

        writer.writerows(rows)

        offset = offset + 20

        print('{}/{}'.format((i+1)*20, 113*20))
