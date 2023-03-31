import csv

# Define the path to the input and output CSV files
input_file = 'abstracts/bme_abstracts_real.csv'
output_file = 'abstracts/bme_abstracts_real_1.csv'

# Define the words to be removed
remove_words = ['darba tēma', 'darba nosaukums']

# Read the input CSV file and create a list of dictionaries
with open(input_file, mode='r', encoding='utf-8', newline='') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)

# Modify the 'abstracts' column by removing sentences containing the remove_words
for row in rows:
    abstracts = row['abstract']
    sentences = abstracts.split('.')
    sentences = [s.strip() for s in sentences if not any(w in s for w in remove_words)]
    row['abstract'] = '. '.join(sentences)

# Write the modified data to a new CSV file
with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(rows)
