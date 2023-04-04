from bs4 import BeautifulSoup
import requests
import warnings
import csv

warnings.filterwarnings('ignore', message='Unverified HTTPS request is being made')

offset = 474
row_id = 1
file = open('abstracts/df_abstracts_real.csv', 'a', encoding='utf-8', newline='\n')
writer = csv.writer(file)

for i in range(100):
    response = requests.get('https://dspace.lu.lv/dspace/handle/7/5279/recent-submissions?'
                            'offset=' + str(offset), verify=False)  # 474
    # response = requests.get('https://dspace.lu.lv/dspace/handle/7/5283/recent-submissions?'
    #                         'offset=' + str(offset), verify=False)  # 442
    # response = requests.get('https://dspace.lu.lv/dspace/handle/7/72/browse?order=DESC&rpp=20&sort_by=2&etal=-1&'
    #                         'offset=' + str(offset) + '&type=dateissued', verify=False)  # 600
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

        abst = text.replace('\n', '')
        abstracts.append(abst)

    # print(len(titles), titles)
    # print(len(abstracts), abstracts)
    # print(len(keywords), keywords)

    for j in range(len(abstracts)):
        rows.append([row_id, titles[j], abstracts[j], 0])
        row_id = row_id + 1

    writer.writerows(rows)
    offset = offset + 20
    print('{}/{}'.format((i + 1) * 20, 100 * 20))

# mod_wsgi-express start-server web/api.py
