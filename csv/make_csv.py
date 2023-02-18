import csv

rows = [
    ['id', 'title', 'abstract_latvian', 'abstract_foreign', 'is_generated']
]

with open('../abstracts.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)
